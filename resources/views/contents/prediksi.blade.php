@extends("layouts.app")

@section("content")
<style>

p.form_text1>span {
    display: inline-block;
    min-width: 80px;
}
    p.form_text2>span {
    display: inline-block;
    min-width: 85px;
}

</style>

<?php $val=1 ?>
<div class="content-wrapper">
              <div class="page-header">
                <h3 class="page-title">
                  <span class="page-title-icon bg-gradient-primary text-white me-2">
                    <i class="mdi mdi-chart-areaspline"></i>
                  </span> Prediksi
                  <link rel="stylesheet" type="text/css" href="css/water.css">
                </h3>
              </div>
              <div class="row">
                <div class="col-md-12 grid-margin stretch-card">
                  <div class="card">
                    <div class="card-body">
                      <h1 style="text-align: center;">Grafik Ketinggian Air</h1>
                      <!-- <img src="assets/images/dash.jpg" class="img-fluid"> -->
                      </div>
                      <!-- <div class="container">
                      <div class="water_wave"></div> -->
                      <main>
  
  <div class="circle-container">
    <div class="circle"></div>
    <div class="wave _{{$valLevel}}"></div>
    <div class="wave _{{$valLevel}}"></div>
    <div class="wave _{{$valLevel}}"></div>
    <div class="wave-below _{{$valLevel}}"></div>
    <div class="desc _1">
      <h2>Level Permukaan Air</h2>
      <p>
        <b>{{$dataLevel}}<span>m</span></b>
      </p>
    </div>
  </div>
  <div class="circle-container">
    <div class="circle"></div>
    <div class="wave _{{$valDebit}}"></div>
    <div class="wave _{{$valDebit}}"></div>
    <div class="wave _{{$valDebit}}"></div>
    <div class="wave-below _{{$valDebit}}"></div>
    <div class="desc _1">
      <h2>Level Debit</h2>
      <p>
        <b>{{$dataDebit}}<span>m</span></b>
      </p>
    </div>
  </div>
  <div class="circle-container">
    <div class="circle"></div>
    <div class="wave _{{$valCurah}}"></div>
    <div class="wave _{{$valCurah}}"></div>
    <div class="wave _{{$valCurah}}"></div>
    <div class="wave-below _{{$valCurah}}"></div>
    <div class="desc _1">
      <h2>Level Curah Hujan</h2>
      <p>
        <b>{{$dataCurah}}<span>m</span></b>
      </p>
    </div>
  </div>
  <div class="circle-container">
    <div class="circle"></div>
    <div class="wave _{{$valKeseluruhan}}"></div>
    <div class="wave _{{$valKeseluruhan}}"></div>
    <div class="wave _{{$valKeseluruhan}}"></div>
    <div class="wave-below _{{$valKeseluruhan}}"></div>
    <div class="desc _1">
      <h2>Level Db + Ch</h2>
      <p>
        <b>{{$dataCurahDebit}}<span>m</span></b>
      </p>
    </div>
  </div>
</main>
                    </div>
                    </div>
                  </div>
        </div>
                 

             

          

 @endsection