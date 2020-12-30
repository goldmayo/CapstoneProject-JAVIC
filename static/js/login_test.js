function SendData(){
    // console.log("Start sendData")
    var usr_id = $("#user-id").val();
    var usr_pw = $("#user-pw").val();
    // console.log(usr_id);
    // console.log(usr_pw);
    if (usr_id=="" || usr_pw==""){
        return;
    }
    $.ajax({
        url:'/ajax_login',
        type:'POST',
        dataType:'JSON',
        contentType:"application/json; charset=UTF-8",
        data: JSON.stringify({name:usr_id, passwd:usr_pw}),
        success:function(res){
            console.log(res);
	    
	    if (res === "200"){
                window.location.href = "chatbot";
            }
            else if(res === "100"){
                alert("open API 서비스 실행 오류입니다.");
            }
            else if(res === "101"){
                alert("암호가 일치하지 않습니다.");
            }
            else if(res === "102"){
                alert("등록된 사용자가 아닙니다.");
            }
            else if(res === "103"){
                alert("동명의 사용자가 존재합니다.");
            }
            else if(res === "104"){
                alert("허가되지 않은 IP주소로부터의 접근입니다.");
            }
            else if(res === "105"){
                alert("휴면 계정입니다.");
            }
            else if(res === "106"){
                alert("계정 사용 기간이 만료되었습니다.");
            }
            else if(res === "107"){
                alert("일시적으로 로그인이 불가합니다.");
            }
            else{
                alert("내부 시스템 오류로 인해 로그인이 불가합니다");
            }

        },
        error:function(error){
            console.log(error);
            console.log("fail");
        }
        
    });
    // console.log("End sendData");
};

$(document).ready(function(){

    $('#send-btn').on('click',function(){
        console.log("start click event handler");
        SendData();
        console.log("end click event handler");
    });

});
