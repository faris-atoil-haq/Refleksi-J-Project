@extends("layouts.app")

@section("content")
<div class="content-wrapper">
            <div class="page-header">
                <h3 class="page-title">
                    <span class="page-title-icon bg-gradient-primary text-white me-2">
                      <i class="mdi mdi-database"></i>
                    </span> Database
                  </h3>
            </div>
          
            <div class="page-body">
                <div class="container-xl">
                    <div class="row row-cards">
                        <div class="col-md-2">
                            <div class="row row-cards">
                                
                                    <div class="card">
                                        <div class="card-body px-0">
                                            <div class="d-flex justify-content-between align-items-center mb-2">
                                                <div class="subheader mb-0"><label class="form-label mb-0">Pilih Kategori</label> </div>
            
                                            </div>
                                            <div class="h3 m-0">
                                                <form action="" method="post" accept-charset="utf-8">
                                                
                                                <select type="text" name="id_kategori" class="form-select" placeholder="Pilih Kategori" onchange="this.form.submit()" id="select-pos2" value=" ">
                                                    <option disabled selected>Pilih Kategori</option>
                                                                                            <option value="1" selected>Level Air</option>
                                                                                            <option value="2" >Curah Hujan</option>
                                                                                            <option value="3" >Debit Air</option>
                                                                                        </select>
                                                </form>
                                            </div>
                                        </div>
                                    </div>

                                   
                                    <div class="card mt-4">
                                    <form action="{{route('database.filter')}}" method='post'>
                                    @csrf
                                        <div class="card-body px-0">
                                            <div class="d-flex justify-content-between align-items-center mb-2">
                                                <div class="subheader mb-0"><label class="form-label mb-0">Tanggal</label> </div>
            
                                            </div>
                                            <div class="h3 m-0">
                                                <form action="" method="post" accept-charset="utf-8">
                                                <input type="date" name="date" value='{{$datanow}}' class="form-control">
                                            </div>
                                        </div>
                                        <button type='submit' class="btn btn-success"> filter</button>

                                        </form>
                                    </div>


                                  
                                    
                                </div>
                            </div>

                        <div class="col-md-10">
                            <div class="card">
                                <div class="card-body">
                                                            <h5 class="card-title">Monitoring</h5>
                                    <div class="table-responsive">
                                        <table class="table table-vcenter table-bordered">
                                            <thead>
                                                <tr>
                                                    <th style=" position: sticky;left: 0;background-color:#f8fafc;" rowspan="2">Zona</th>
                                                    <th colspan="24" class="text-center">Jam</th>
                                                </tr>
                                                <tr>
                                                @foreach($data as $row)
                                                <th class="text-center">{{ $row->created_at}}</th>
                                                @endforeach
                                                   
                                                                                           
                                                                                            <!-- <th class="text-center">01:00</th>
                                                                                            <th class="text-center">02:00</th>
                                                                                            <th class="text-center">03:00</th>
                                                                                            <th class="text-center">04:00</th>
                                                                                            <th class="text-center">05:00</th>
                                                                                            <th class="text-center">06:00</th>
                                                                                            <th class="text-center">07:00</th>
                                                                                            <th class="text-center">08:00</th>
                                                                                            <th class="text-center">09:00</th>
                                                                                            <th class="text-center">10:00</th>
                                                                                            <th class="text-center">11:00</th>
                                                                                            <th class="text-center">12:00</th>
                                                                                            <th class="text-center">13:00</th>
                                                                                            <th class="text-center">14:00</th>
                                                                                            <th class="text-center">15:00</th>
                                                                                            <th class="text-center">16:00</th>
                                                                                            <th class="text-center">17:00</th>
                                                                                            <th class="text-center">18:00</th>
                                                                                            <th class="text-center">19:00</th>
                                                                                            <th class="text-center">20:00</th>
                                                                                            <th class="text-center">21:00</th>
                                                                                            <th class="text-center">22:00</th>
                                                                                            <th class="text-center">23:00</th> -->
                                                                                        </tr>
                                            </thead>
                                            <tbody>
                                                  <tr>
                                                    <td  class="d-flex justify-content-between" style="white-space: nowrap;">
                                                       <a>Zona 1 </a>
                                                        
                                                         
                                                    </td>
                                                    @foreach($data as $row)
                                                    <td class="text-center text-dark fw-bold" style="background-color:white">
                                                                                                        <div class="d-flex justify-content-center mb-0" style="font-size:12px">{{ $row->level}} <span class="ps-1">mm</span> </div>	
                                                                                                    
                                                    </td>
                                                    @endforeach
                                                                                            
                                                                                            
                                                  </tr>
                                              </tbody>
                                     
                          </table>
                      </div>
<div class="col-xl-9">
<div class="row gx-2">
    <div class="col-xl-2 col-6">
        <div class="row h-100 gx-2 pt-2 pt-lg-2">
            <div class="col-3">
                <div class="rounded border border-dark" style="background-color:white;height:35px;"></div>
            </div>
            <div class="col-9 d-flex align-items-center">
                <h5 class="mb-0">Tidak Hujan</h5>
            </div>

        </div>
    </div>
    <div class="col-xl-2 col-6">
        <div class="row h-100 gx-2 pt-2 pt-lg-2">
            <div class="col-3">
                <div class="rounded border border-dark" style="background-color:#70cddd;height:35px;"></div>
            </div>
            <div class="col-9 d-flex align-items-center">
                <h5 class="mb-0">Hujan Sangat Ringan</h5>
            </div>

        </div>
    </div>
    <div class="col-xl-2 col-6">
        <div class="row h-100 gx-2 pt-2 pt-lg-2">

            <div class="col-3">
                <div class="rounded border border-dark" style="background-color:#35549d;height:35px"></div>
            </div>
            <div class="col-9 d-flex align-items-center">
                <h5 class="mb-0">Hujan Ringan</h5>
            </div>
        </div>
    </div>
    <div class="col-xl-2 col-6">
        <div class="row h-100 gx-2  pt-2 pt-lg-2">
            <div class="col-3">
                <div class="rounded border border-dark" style="background-color:#fef216;height:35px"></div>
            </div>
            <div class="col-9 d-flex align-items-center">
                <h5 class="mb-0">Hujan Sedang</h5>
            </div>

        </div>
    </div>
    <div class="col-xl-2 col-6">
        <div class="row h-100 gx-2 pt-2 pt-lg-2">
            <div class="col-3">
                <div class="rounded border border-dark" style="background-color:#f47e2c;height:35px"></div>
            </div>
            <div class="col-9 d-flex align-items-center">
                <h5 class="mb-0">Hujan Lebat</h5>
            </div>

        </div>
    </div>
    <div class="col-xl-2 col-6">
        <div class="row h-100 gx-2 pt-2 pt-lg-2">
            <div class="col-3">
                <div class="rounded border border-dark" style="background-color:#ed1c24;height:35px"></div>
            </div>
            <div class="col-9 d-flex align-items-center">
                <h5 class="mb-0">Hujan Sangat Lebat</h5>
            </div>

        </div>
    </div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
@endsection