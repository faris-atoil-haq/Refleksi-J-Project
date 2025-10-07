<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PrediksiController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// Route::get('/', function () {
//     return view('welcome');
// });


Route::get('/', [PrediksiController::class, 'home'])->name('home');
Route::get('/dashboard', [PrediksiController::class, 'dashboard'])->name('dashboard');
Route::get('/prediksi', [PrediksiController::class, 'prediksi'])->name('prediksi');
Route::get('/database', [PrediksiController::class, 'database'])->name('database');
Route::get('/database/{date}', [PrediksiController::class, 'databaseDate'])->name('database.date');
Route::post('/database/filter', [PrediksiController::class, 'databaseFilter'])->name('database.filter');
// Route::get('/', [PrediksiController::class, 'index']);
Route::get('/data', [PrediksiController::class, 'getapidata'])->name('apidata');