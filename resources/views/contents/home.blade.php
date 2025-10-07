<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Started</title>
    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Georgia, 'Times New Roman', Times, serif;
        }        
        body{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
            background-color: #1E1F31;
        }
       
        .wrapper{
            position: relative;
            height: 100vh;
            overflow: hidden;
        }
        header{
            padding: 50px 100px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        header ul li{
            list-style: none;
            display: inline-block;
            margin: 0 15px;
        }
        header ul li a{
            color: #aba9b4;
            text-transform: uppercase;
            text-decoration: none;
            letter-spacing: 1px;
            transition: all ease 0.5s;
        }
        header ul li a:hover{
            color: #f09053;
        }
        header ul li a.btn{
            display: inline-block;
            width: 180px;
            height: 60px;
            line-height: 60px;
            background-color: #f09053;
            color: #fff;
            text-align: center;
            font-size: 18px;
            border-radius: 50px;
            transition: all ease 0.5s;
        }
        header ul li a.btn:hover{
            background-color: #615c59;
        }

        .content{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            padding: 50px 100px 0;
        }
        .text{
            width: 70%;
            padding-right: -150px;
        }
        .text p{
            font-size: 28px;
            line-height: 50px;
            color: #fff;
        }
        .text p span{
            color: turquoise;
        }
        .text a{
            position: relative;
            display: inline-block;
            font-size: 18px;
            text-transform: uppercase;
            color: #fff;
            text-decoration: none;
            padding: 18px 45px;
            letter-spacing: 2px;
            font-weight: 500;
            margin-top: 60px;
        }
        .text a:before{
            content: '';
            position: absolute;
            top: 10px;
            left: 30px;
            width: 70px;
            height: 60px;
            border-radius: 50px;
            background-color: lightseagreen;
            z-index: -1;
            transition: all ease 0.5s;
        }
        .text a:hover:before{
            width: 100%;
        }

        section{
            position: relative;
            width: 100%;
        }

        section .waves{
            position: relative;
        }

        section .waves .wave{
            position: absolute;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 100px;
            background: url(assets/images/wave.png);
            background-size: 1000px 100px;
        }
       
        section .waves .wave#wave1{
            opacity: 1;
            bottom: 0;
            z-index: 1000;
            animation: animate 4s linear infinite;
        }

        section .waves .wave#wave2{
            opacity: 0.5;
            bottom: 10px;
            z-index: 999;
            animation: animate2 4s linear infinite;
        }

        section .waves .wave#wave3{
            opacity: 0.2;
            bottom: 15px;
            z-index: 998;
            animation: animate 2s linear infinite;
        }

        section .waves .wave#wave4{
            opacity: 0.7;
            bottom: 20px;
            z-index: 999;
            animation: animate2 2s linear infinite;
        }

        @keyframes animate{
            0%{
                background-position-x: 1000px;
            }
            100%{
                background-position-x: 0px;
            }
        }

        @keyframes animate2{
            0%{
                background-position-x: 0px;
            }
            100%{
                background-position-x: 1000px;
            }
        }

        .bg{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            mix-blend-mode: screen;            
        }

        h1{
            position: absolute;
            bottom: 75vh;
            transform: translateY(50%);
            width: 100%;
            text-align: center;
            color: #fff;
            font-size: 3em;
            font-weight: 100;
            text-transform: uppercase;
        }

        .island{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            width: 650px;
            bottom: 0;
            pointer-events: none;
        }

       
        @keyframes rotation {
            100%{
                transform: rotate(360deg);
            }
        }
    </style>
     <link rel="shortcut icon" href="{{asset('assets/images/its.png')}}" />
</head>
<body>


<div class="wrapper">
    <header>
        <div class="logo">
            <img src="" alt="">
        </div>
    </header>

    <div class="content">
        <div class="text"> 
            <a href="{{route('dashboard')}}" class="btn">Get Started</a>
        </div>
       
    </div>

</div>

<section>
    <div class="waves">
        <img src="assets/images/bg.jpg" class="bg">
        <h1>Prediksi Level <br> Permukaan Air Sungai</h1>
        <img src="assets/images/island.png" class="island">
        <div class="wave" id="wave1"></div>
        <div class="wave" id="wave2"></div>
        <div class="wave" id="wave3"></div>
        <div class="wave" id="wave4"></div>  
    </div>
</section>


</body>
</html>