const express = require('express')
const app = express()
const path = require('path')
var request = require('request')

app.set('views', path.join(__dirname, 'views')); // ejs file location
app.set('view engine', 'ejs'); //select view templet engine

app.use(express.static(path.join(__dirname, 'public')));//to use static asset

app.use(express.json());
app.use(express.urlencoded({extended:false}));



app.get('/test', function(req, res){ // chart1 사이트 데이터 테스트
    res.render('test')
})


app.get('/test2',function(req,res){  // chart2 사이트 데이터 테스트
 
    
 
    res.render('test2');

})



app.get('/test3', function(req, res){ // ejs 데이터  테스트
    //http://localhost:3000/test3?data=%22%EC%95%84%EB%85%95%22 
     var ss = req.query.data; //챗봇에서 받아오는 데이터
    res.render('test3',{data:ss})
})



app.get('/chart',function(req,res){  //일반 신용 대출 금리 사이트
 
    // var ss = req.query.rating; //챗봇에서 받아오는 데이터
    // console.log(ss)
    res.render('chart'); 

})


app.get('/chart2',function(req,res){ //원리금 균등 사이트
 

    //챗봇에서 데이터 받아온다음 신용등급을 페이지에 렌더링하면서 넘겨주고 그 값을 다시 ajax로 파이썬 서버에 던져줘야함
    
    res.render('chart2'); 

})




app.get('/chart3',function(req,res){ //만기일시 균등 사이트
 

    //챗봇에서 데이터 받아온다음 신용등급을 페이지에 렌더링하면서 넘겨주고 그 값을 다시 ajax로 파이썬 서버에 던져줘야함
    
    res.render('chart3'); 

})



app.get('/chart4',function(req,res){ //원금 균등 사이트
 

    //챗봇에서 데이터 받아온다음 신용등급을 페이지에 렌더링하면서 넘겨주고 그 값을 다시 ajax로 파이썬 서버에 던져줘야함
    
    res.render('chart4'); 

})

app.get('/chart5', function(req,res){

    res.render('chart5');

})

app.get('/public', function(req, res){
    res.render('public');
})



app.listen(3000)
