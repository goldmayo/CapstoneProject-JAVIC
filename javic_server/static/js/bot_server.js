var isEmpty = function(value){ 
    if( value == "" || value == null || value == undefined || ( value != null && typeof value == "object" && !Object.keys(value).length ) ){ 
        return true 
    }else{ 
        return false 
    } 
};

function show_menu(){
    let current_time = new Date();
    appendChatbox("메뉴",fromServer=false);
    var menu = '<div class="col-12 m-0 p-2"><div class="bot-response" data-is'+current_time.toLocaleTimeString()+'><div class="row m-0 p-2"><div class="col-2"><img class="bot-img float-left" src="/static/images/domado.jpg"></div></div><a class="float-left ml-4 border"><p>안녕하세요. 챗봇 서비스 자빅 (JAVIC) 입니다.</p><p>조회하시고자 하시는 메뉴를 선택하시거나, 채팅창에 자유롭게 질문 내용을 입력해주세요.</p><p>대화 도중 안내 메뉴를 확인하시려면 메뉴 버튼을 선택해주세요.</p><div class="service-menu m-1 p-1"><div class="row m-0 p-0"><div class="col-xs-12 col-md-6 col-lg-6 m-0 p-1"><button class="btn btn btn-outline-secondary w-100" type="button" value="draft-vacation"><i class="fa fa-bed" aria-hidden="true"></i><strong>휴가 신청</strong></button></div><div class="col-xs-12 col-md-6 col-lg-6 m-0 p-1"><button class="btn btn-outline-secondary w-100" type="button" value="mail-check"><i class="fa fa-envelope" aria-hidden="true"></i><strong>메일 확인</strong></button></div></div></div></a></div></div>';
    

    setTimeout(function(){
        $("#msg-goes-here").append(menu);
        $(".chatbot-body").scrollTop($(".chatbot-body")[0].scrollHeight);//스크롤 최하단으로
    },600);
    // $("#msg-goes-here").append(menu);
    //console.log(user_choice);
    //console.log(menu)
    //$(".chatbot-body").scrollTop($(".chatbot-body")[0].scrollHeight);//스크롤 최하단으로
}
function appendConfirm(text){
    let current_time = new Date();
    var chat = $('<div class="col-12 m-0 p-2"></div>');
    var bot_user = $('<div class="bot-response"><div class="row m-0 p-2"><div class="col-2"><img class="bot-img float-left" src="/static/images/domado.jpg"></div></div></div>');
    var a_tag = $('<a class="float-left ml-4 border"></a>');
    var p_tag = $('<p></p>');
    var text = document.createTextNode(text);
    var confirm_btns= $('<div class="service-menu m-1 p-1"><div class="row m-0 p-0"><div class="col-xs-12 col-md-6 col-lg-6 m-0 p-1"><button class="btn btn btn-outline-secondary w-100" value="yes-btn"><strong>네.</strong></button></div><div class="col-xs-12 col-md-6 col-lg-6 m-0 p-1"><button class="btn btn-outline-secondary w-100" value="cancel-btn"><strong>아니오.</strong></button></div></div></div>');
    bot_user.attr('data-is', current_time.toLocaleTimeString());
    p_tag.append(text);
    a_tag.append(p_tag);
    a_tag.append(confirm_btns);
    bot_user.append(a_tag);
    chat.append(bot_user);

    $('#msg-goes-here').append(chat);
    $(".chatbot-body").scrollTop($(".chatbot-body")[0].scrollHeight);
}

function appendChatbox(text,fromServer=false){

    let current_time = new Date();
    var chat = $('<div class="col-12 m-0 p-2"></div>');
    console.log(chat);
    var bot_user = $('<div></div>');
    var a_tag = $('<a></a>');
    var text = document.createTextNode(text);
    
    if(fromServer==true){
        bot_user.addClass('bot-response');
        bot_user.attr('data-is', current_time.toLocaleTimeString());
        bot_user.append('<div class="row m-0 p-2"><div class="col-2"><img class="bot-img float-left" src="/static/images/domado.jpg"></div></div>');
        a_tag.addClass("float-left ml-4 border");
    }
    else{
        bot_user.addClass('user-request');
        bot_user.attr('data-is', current_time.toLocaleTimeString());
        a_tag.addClass("float-right");
    }
    a_tag.append(text);
    bot_user.append(a_tag);
    chat.append(bot_user);

    $('#msg-goes-here').append(chat);
    $(".chatbot-body").scrollTop($(".chatbot-body")[0].scrollHeight);//스크롤 최하단으로
}

function appendMailList(lists){
    let current_time = new Date();
    var div =  $('<div class="col-12 m-0 p-2"></div>');
    var botresp = $('<div class="bot-response float-left"></div>');
    var corpus = $('<a></a>');
    var text = document.createTextNode(text);
    var mail_List = $('<ol></ol>'); //순서

    for(var i= 0; i < lists.length; i++){
        var mail_Item = $('<li></li>');
        var text = document.createTextNode(lists[i]);

        mail_Item.append(text);
        mail_Item.append("<br><br>");

        mail_List.append(mail_Item);
    }
    corpus.append("[ 최근 읽지 않은 메일이 "+lists.length+"개 있습니다 ]");
    corpus.append(mail_List);
    corpus.append("확인하실 메일 번호를 입력해주세요 :)");
    botresp.attr('data-is', current_time.toLocaleTimeString());// data-is가 시간을 나타내는 속성이므로 추가
    botresp.append('<div class="row m-0 p-2"><div class="col-2"><img class="bot-img float-left" src="/static/images/domado.jpg"></div></div>');
    botresp.append(corpus);
    div.append(botresp);

    $('#msg-goes-here').append(div);
    $(".chatbot-body").scrollTop($(".chatbot-body")[0].scrollHeight);//스크롤 최하단으로
}

function appendSummarizedSentences(lists){
    let current_time = new Date();
    var div =  $('<div class="col-12 m-0 p-2"></div>');
    var botresp = $('<div class="bot-response float-left"></div>');
    var corpus = $('<a></a>');
    var text = document.createTextNode(text);
    var sentence_List = $('<ol></ol>');

    for(var i = 0; i < lists.length; i++){
	    var sentence_Item = $('<li></li>');
	    var text = document.createTextNode(lists[i]);
	    
	    sentence_Item.append(text);
	    
	    if (i < lists.length - 1) {
		    sentence_Item.append("<br><br>");
	    }

	    sentence_List.append(sentence_Item);
    }
    corpus.append("[ " + lists.length + "줄 요약 결과입니다 :) ]");
    corpus.append(sentence_List);
    botresp.attr('data-is', current_time.toLocaleTimeString());
    botresp.append('<div class="row m-0 p-2"><div class="col-2"><img class="bot-img float-left" src="/static/images/domado.jpg"></div></div>');
    botresp.append(corpus);
    div.append(botresp);

    $('#msg-goes-here').append(div);
    $(".chatbot-body").scrollTop($(".chatbot-body")[0].scrollHeight);
}

function Do_Actions(actions){

    for(i=0; i < actions.length; i++){
        if(actions[i]["behavior"] === "logout"){
            window.location.href = actions[i]["logout_link"];
        }
    }
}

$(document).on("click", "button", function(){
    var myText;
    if (this.value == "send-btn") { //평문
        console.log($(this).val());
        console.log(document.getElementById("user-input").value);
        console.log($("user-input").val());
        myText = $("user-input").val();
        SendData(myText);
    }
    if (this.value == "menu-btn") { // 메뉴
        myText = $(this).text();
        console.log(myText);
        show_menu();
    }
    if (this.value == "draft-vacation") { //휴가신청
        myText = $(this).text();
        console.log(myText);
        console.log($(this).val());
        SendData(myText);
    }
    if (this.value == "mail-check") { //메일확인
        myText = $(this).text();
        console.log(myText);
        SendData(myText);
    }
    if (this.value == "cancel-btn") { // 취소
        myText = $(this).text();
        console.log(myText);
        SendData(myText);
    }
    if (this.value == "yes-btn") { // 확인
        myText = $(this).text();
        console.log(myText);
        SendData(myText);
    }
    if (this.value == "quit-btn") { // 종료 현재는 핸디로그아웃 > 핸디로그아웃시 로그인페이지로
        myText = $(this).text();
        console.log(myText);
        SendData("핸디로그아웃");
    }
});

function SendData(mText){
    console.log("myText :",mText);
    if (isEmpty(mText)){
        return;
    }
    appendChatbox(mText);
    $.ajax({
        url:'./req',
        type:'POST',
        dataType:'JSON',
        header:{
            "Content-Type":"application/json; charset=euc-kr"
        },
        contentType: "application/json",
        data:JSON.stringify({text:mText}),
        success:function(res){
		var header = res["header"]["message_type"]; //서비스타입체크 
		console.log(header)
		if (header == "plain text") { // 평문
			console.log(res["content"]);
			appendChatbox(res["content"],true);
		}
		else if (header == "latest mails") {
			console.log(res["content"]);
			appendMailList(res["content"], true);
		}
		else if (header == "confirm") { //yes or no 사용자의 진행 의사확인
			console.log(res["content"]);
			appendConfirm(res["content"]);
		} 
		else if (header == "logout_message") { // handylogout
			appendChatbox(res["content"],true);
                // Do_Actions(res["afer_content"]["actions"]);
			setTimeout(Do_Actions, res["after_content"]["recommended_delay_ms"], res["after_content"]["actions"]);
		}
		// INYEONG
		else if (header == "summarized" ) {
			console.log(res["content"]);
			appendSummarizedSentences(res["content"], true);
		}
		///////
		else {
			console.log("no plain text response")
		}

        },
        error:function(error){
            console.log("communication error");
            console.log(error);
        }
    });
    //$("#user-input").val() == null;
    document.getElementById("user-input").value = null;//사용자 입력 리셋
}

function scrollBottom(){
    $(".chatbot-body").scrollTop($(".chatbot-body")[0].scrollHeight);//스크롤 최하단으로
}

$(document).ready(function(){
    $("#user-input").keypress(function (e) {
        if (e.which == 13){
            var usrInput = $("#user-input").val();
            SendData(usrInput);  // 실행할 이벤트
        }
    });

});
