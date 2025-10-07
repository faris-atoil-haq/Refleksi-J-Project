<?php

namespace App\Http\Controllers;

use App\Models\Curah;
use App\Models\Debit;
use Illuminate\Http\Request;
use App\Models\Water;
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

class PrediksiController extends Controller
{
    public function home(){
        return view('contents.home');
    }

    public function dashboard(){

        // dd('dashboard');
        $data = Water::get();

        $datanow = Carbon::now();
        $data = Water::latest('created_at')->take(5)->get();
        $data1 = Curah::latest('created_at')->take(5)->get();
        $data2 = Debit::latest('created_at')->take(5)->get();

         //dd($datanow->format('Y-m-d'));

         $val = Curah::first();
         $val1 = Water::first();
         $val2 = Debit::first();

        $valCurah = $val->curah;
        $valLevel = $val1->level;
        $valDebit = $val2->debit;


        view()->share([
            'data' => $data,
            'data1' => $data1,
            'data2' => $data2,
            'datanow' => $datanow->format('Y-m-d')
        ]);

        return view('contents.dashboard');
    }

    public function prediksi(){
         //dd('sss');
         $data = Water::get();

        $datanow = Carbon::now();
        $data = Water::whereDate('created_at', '=',$datanow->format('Y-m-d'))->get();
        $data1 = Curah::whereDate('created_at', '=',$datanow->format('Y-m-d'))->get();
        $data2 = Debit::whereDate('created_at', '=',$datanow->format('Y-m-d'))->get();
        
        
        $val0 = Curah::latest()->first();
        $val1 = Water::latest()->first();
        $val2 = Debit::latest()->first();

        $konstanta = 49430;
        $valCurah = $val0->curah;
        $valCurah = $valCurah / 1000;
        $valLevel = $val1->level;
        $valLevel = $valLevel / 100;
        $valDebit = $val2->debit;
        
        $valLevel = number_format((float)($valLevel), 4, '.', '');

        $hasilCurah = $valCurah + $valLevel;
        $hasilCurah = number_format((float)($hasilCurah), 4, '.', '');

        $hasilDebit = ( ( $konstanta * $valLevel ) + $valDebit ) / $konstanta;
        $hasilDebit = number_format((float)($hasilDebit), 4, '.', '');
        
        $hasilKeseluruhan = $valCurah + $hasilDebit;
        $hasilKeseluruhan = number_format((float)($hasilKeseluruhan), 4, '.', '');


        $val = [];
        $val[0] = $valLevel*100/5;
        $val[1] = $hasilCurah*100/5;
        $val[2] = $hasilDebit*100/5;
        $val[3] = $hasilKeseluruhan*100/5;
        
        
        for ($sum=0;$sum<4;$sum++){
            $cnt = 0;

            for ($i = 0; $i <= 100; $i=$i+10) {
                // echo $i;
                
                if ($val[$sum] > $i)
                {
                    $cnt++;
                }
                else 
                    break;
            }

            if ($val[$sum] == ($cnt))
                $val[$sum+4] = ($cnt)*10;
            else if ($val[$sum] < $cnt*10+5)
                $val[$sum+4] = ($cnt-1)*10+5;
            else
                $val[$sum+4] = ($cnt-1)*10;
        // echo $val[$sum+4];
        // echo "\n";
        $val[$sum+4] = $val[$sum+4]-5;
        }
         //dd($datanow->format('Y-m-d'));

        view()->share([
            'data' => $data,
            'dataLevel' => $valLevel,
            'dataCurah' => $hasilCurah,
            'dataDebit' => $hasilDebit,
            'dataCurahDebit' => $hasilKeseluruhan,

            'valLevel' => $val[4],
            'valCurah' => $val[5],
            'valDebit' => $val[6],
            'valKeseluruhan' => $val[7],

            'datanow' => $datanow->format('Y-m-d')
        ]);
        
        return view('contents.prediksi');
    }

    public function database(){

         //dd('sss');
        $data = Water::get();

        $datanow = Carbon::now();
        $data = Water::whereDate('created_at', '=',$datanow->format('Y-m-d'))->get();

         //dd($datanow->format('Y-m-d'));

        view()->share([
            'data' => $data,
            'datanow' => $datanow->format('Y-m-d')
        ]);

        return view('contents.database');
    }

    public function databaseFilter (Request $request){

        $data = Water::whereDate('created_at', '=', $request->date)->get();

        // dd($data);
        $datanow = Carbon::now();

        // dd($datanow->format('Y-m-d'));

        view()->share([
            'data' => $data,
            'datanow' => $datanow->format('Y-m-d')
        ]);

        return view('contents.database');

    }

    public function databaseDate($date){

        // dd('sss');
        $datanow = Carbon::now();
        $data = Water::whereDate('created_at', '=',$datanow->format('Y-m-d'))->get();

        dd($data);
        // dd($datanow->format('Y-m-d'));

        view()->share([
            'data' => $data,
            'datanow' => $datanow->format('Y-m-d')
        ]);

        return view('contents.database');
    }

    public function getapidata() {
        $response = Http::get('https://www.rainits.com/'); // Ganti URL dengan URL situs web yang ingin Anda ambil datanya

    if ($response->successful()) {
        $data = $response->json(); // Mengambil data JSON dari respons
        return response()->json($data); // Mengembalikan data dalam format JSON sebagai respons API
    } else {
        return response()->json(['error' => 'Failed to retrieve data'], 500); // Mengembalikan respons error jika gagal mendapatkan data
    }
    }
    
}
