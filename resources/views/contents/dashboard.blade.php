@extends("layouts.app")

@section("content")
<!-- partial -->
<div class="content-wrapper">
            <div class="page-header">
              <h3 class="page-title">
                <span class="page-title-icon bg-gradient-primary text-white me-2">
                  <i class="mdi mdi-home"></i>
                </span> Dashboard
              </h3>
            </div>
            <div class="row">
              <div class="col-lg-6 grid-margin stretch-card">
                <div class="card">
                  <div class="card-body">
                    <h4 class="card-title" style="text-align: center;">Level Air</h4>
                    <canvas id="lineChart" class="chartjs" width="undefined" height="undefined"></canvas>
                  </div>
                </div>
              </div>
              <div class="col-lg-6 grid-margin stretch-card">
                <div class="card">
                  <div class="card-body">
                    <h4 class="card-title" style="text-align: center;">Curah Hujan</h4>
                    <canvas id="lineChartDark" class="chartjs" style="height:230px"></canvas>
                    <!-- <canvas id="lineChart" class="chartjs" width="undefined" height="undefined"></canvas> -->
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-6 grid-margin stretch-card">
                <div class="card">
                  <div class="card-body">
                  <h4 class="card-title">Level Air Status</h4>
                    <div class="table-responsive">
                      <table class="table">
                        <thead>
                          <tr>
                            <th> Waktu </th>
                            <th> Akumulasi Level Hujan </th>
                          </tr>
                        </thead>
                        <tbody>
                          @foreach($data as $row)
                          <tr>
                            <td> {{$row->created_at}} </td>
                            <td> {{$row->level}} cm </td>
                          </tr>
                          @endforeach
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-lg-6 grid-margin stretch-card">
                <div class="card">
                  <div class="card-body">
                  <h4 class="card-title">Curah Hujan Status</h4>
                    <div class="table-responsive">
                      <table class="table">
                        <thead>
                          <tr>
                            <th> Waktu </th>
                            <th> Akumulasi Curah Hujan </th>
                          </tr>
                        </thead>
                        <tbody>
                          @foreach($data1 as $row)
                          <tr>
                            <td> {{$row->created_at}} </td>
                            <td> {{$row->curah}} m </td>
                          </tr>
                          @endforeach
                        </tbody>                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
           
          </div>
          
      
          
          <!-- content-wrapper ends -->
@endsection
