# -*- coding: utf-8 -*-

from flask import Flask

import requests, xmltodict, json, datetime

from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from flask_restful import Resource, Api

from flask_restful import reqparse

from xml.etree.ElementTree import parse

import xml.etree.ElementTree as ET

from lxml import etree

import redis



class Draft_vacation(Resource):

    def get(self):

        try:

            r=redis.StrictRedis(host="db", port=6379, db=0)

            parser = reqparse.RequestParser()

            parser.add_argument('draft_sdate', type=str)

            parser.add_argument('draft_edate', type=str)

            parser.add_argument('key', type=str)

            args = parser.parse_args()

           

            _draftsdate= args['draft_sdate']

            _draftedate= args['draft_edate']

            _userkey= args['key']

            



            json_user_data = r.get(_userkey).decode('utf-8')

            user_data = json.loads(json_user_data)

            # 휴가신청서 서식아이디

            formId = "JHOMS193170028328000"



            def draft_vacation_():

                try:

                    

                    root = setHox(user_data)

                    setBody(user_data)

                    #ET.dump(root)

                    url = "http://123.212.190.148:8300/bms/cz/cb/prc/OpenAPIProcDoc.act"

                    files = {'hoxfile': open("data/"+user_data["session"]["empcode"]+"hox.xml", 'rb'), 'bodyfile': open("data/"+user_data["session"]["empcode"]+"bodyfile", 'rb')}

                    values = {'K':_userkey, 'CMD':'draftDoc', 'FORMID':formId}

                    r = requests.post(url, files=files, data=values)



                except IOError as e:

                    return 'Error:{}'.format(e) ,404

                

            def setHox(user_data):

                

                hoxfile = "data/hoxDraft.xml"

                tree = parse(hoxfile)

                root = tree.getroot()

                

                sdate = datetime.datetime.strptime(_draftsdate, "%Y%m%d").date()

                edate = datetime.datetime.strptime(_draftedate, "%Y%m%d").date()

                period = (edate-sdate).days+1

                

                # 휴가신청서 제목

                title = "휴가신청서("+user_data["session"]["name"]+", 연차, "+ _draftsdate + "~" + _draftedate + ", " + str(period) + "일)"



                # 서식정보 설정

                h_formId = root.find("./docInfo/formInfo/formID")

                if h_formId is not None:

                    h_formId.text = formId

            

                # 제목 설정

                h_title = root.find("./docInfo/title")

                if h_title is not None:

                    h_title.text = title



                # 결재선 설정

                setApprovalFlow(root)



                # 수신자 설정

                setReceipient(root)



                output = ET.tostring(root, encoding='UTF-8', method='xml')

                x_header = '<?xml version="1.0" encoding="UTF-8"?>\n'

                f = open("data/"+user_data["session"]["empcode"]+"hox.xml", 'w', encoding='utf-8')

                f.write(x_header + output.decode('utf-8'))

        

                return root



            def setApprovalFlow(root):

                h_af = root.find("./approvalFlow")

                if h_af is None:

                    root.append(ET.Element("./approvalFlow"))

                participant = ET.SubElement(h_af, "participant")

                p_ID = ET.SubElement(participant, "ID")

                p_ID.text = "004127302"

                p_type = ET.SubElement(participant, "type")

                p_type.text = "user"

                p_at = ET.SubElement(participant, "approvalType")

                p_at.text = "user_approval"



            def setReceipient(root):

                h_receiptRoot = root.find("./docInfo/content/receiptInfo")

                h_receiptInfo = h_receiptRoot.find("./recipient")



                if h_receiptInfo is None:

                    h_receiptRoot.append(ET.Element("recipient"))

                    h_receiptInfo = h_receiptRoot.find("./recipient")

                h_rec = ET.SubElement(h_receiptInfo, "rec")

                h_rec.set("type", "rectype_dept")

                h_recID = ET.SubElement(h_rec, "ID")

                h_recID.text = "500609344"



            def setBody(user_data):

                # 본문파일저장 

                bodydata = _draftsdate + "~" + _draftedate + " 까지 개인적인 사정으로 휴가를 신청합니다."

                f = open("data/"+user_data["session"]["empcode"]+"bodyfile", 'w', encoding='utf-8')

                f.write(bodydata)



            

            draft_vacation_()

            return '휴가 기안 작성이 완료되었습니다. ',200

                

        except Exception as e:

            return {'error': str(e)},404











