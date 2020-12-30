import json
def wrapContent(content,after=None,type="plain text"):
    #print("content :",content)
    rst = {"header":{"message_version":"0.0.1b","message_type":type},"content":content}
    if(after is None):
        rst["after_content"] = {"recommended_delay_ms":0,"actions":[]}
    else:
        rst["after_content"] = after
    return json.dumps(rst,ensure_ascii=False,indent=3)
    #로그인할 때 api 서버에서 받은 key를 던져준다