#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from google.appengine.api import urlfetch
import json
import jinja2
import cgi
import logging


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        #self.response.write(tmpl.render(network=network))
        self.response.out.write("""
                                <html>
                                  <head>
                                    <title>
                                      STEP hw6
                                    </title>
                                  <head>
                                  <body>
                                    STEP Homework 6<br><br>
                                    <form action="/input1" method="get">
                                      <input type="submit" value="Alternate Words">
                                    </form>
                                    <form action="/input2" method="get">
                                      <input type="submit" value="Transfer Guide">
                                    </form>
                                  </body>
                                </html>
                                """)



class AlternateWordsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        self.response.out.write("""
                                <html>
                                  <head>
                                    <title>
                                      Alternate Words
                                    </title>
                                  <head>
                                  <body>
                                    Please input characters<br><br>
                                    <form action="/output1" method="post">
                                      <input type="text" name="input1">
                                      </textarea>
                                      <input type="text" name="input2">
                                      </textarea>
                                      <br>
                                      <input type="submit" value="Go">
                                    </form>
                                  </body>
                                </html>
                                """)


class Result_AlternateWordsPage(webapp2.RequestHandler):
    def post(self):
        
        def alternate_words(input1,input2):

            list_input1 = list(input1)
            list_input2 = list(input2)

            if len(list_input1) == len(list_input2):
                output = ""
                for i in range(len(list_input1)):
                    output += list_input1[i]
                    output += list_input2[i]
                return output
            else:
                output = input1 if len(input1) > len(input2) else input2
                min_length_input = input1 if len(input1) < len(input2) else input2
                index = 0
                for i in range(len(min_length_input)):
                    output = output[:i+1+index] + min_length_input[i] + output[i+1+index:]
                    index += 1
                return output
 
        
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        self.response.out.write("""
                                <html>
                                  <head>
                                    <title>
                                      RESULT
                                    </title>
                                  <head>
                                  <body>
                                    Your input words are ... <br>&#x1f693&#x1f695&#x1f693&#x1f695&#x1f693&#x1f695&#x1f693&#x1f695<br>【
                               """)
        output = alternate_words(self.request.get("input1"),self.request.get("input2"))
        self.response.out.write(output)
        self.response.out.write(""" 】
                                  </body>
                                </html>
                                """
                                )



networkJson = urlfetch.fetch("https://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）
        
class TransferGuidePage(webapp2.RequestHandler):
    def get(self):

        

        start_station = jinja2.Template(  # Jinjaのテンプレートエンジンを使ってHTMLを作成
        '''
        <select name="start_station">
          {% for line in network %}
            <option value="line" disabled>==========</option>
            <option value="line" disabled>{{line["Name"]}}</option>        
            {% for station in line["Stations"] %}
            <option value="{{station}}">{{station}}</option>
          {% endfor %}
        {% endfor %}
        </select>
        ''')
        end_station = jinja2.Template(  # Jinjaのテンプレートエンジンを使ってHTMLを作成
        '''
        <select name="end_station">
          {% for line in network %}
          <option value="line" disabled>==========</option>
          <option value="line" disabled>{{line["Name"]}}</option>        
            {% for station in line["Stations"] %}
            <option value="{{station}}">{{station}}</option>
          {% endfor %}
        {% endfor %}
        </select>
        ''')
    

        
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        self.response.out.write("""
                                <html>
                                  <head>
                                    <title>
                                      Transfer Guide
                                    </title>
                                  <head>
                                  <body>
                                    
                                    <form action="/output2" method="post">Departure:<br>
                                """)
        self.response.write(start_station.render(network=network))
        self.response.out.write("""<br>Arrival:<br>
                                """)
        self.response.write(end_station.render(network=network))   
        self.response.out.write("""    
                                    <form action="/output2" method="post">
                                      <br><input type="submit" value="Go">
                                    </form>
                                  </body>
                                </html>
                                """)




class Result_TransferGuidePage(webapp2.RequestHandler):
    
    def post(self):

        def make_station_list():
            station_list = []
            line_list = []
            for line in network:
                line_station = []
                line_list.append(line["Name"])       
                for station in line["Stations"]:
                    line_station.append(station)
                station_list.append(line_station)
            return station_list, line_list

        def search_path(station_list,line_list,start,end):
            path_list = []
            check_station = []
            search_station = [start]
            finish_flag = 0
            for i in range(len(station_list)):
                for j in range(len(station_list[i])):
                    if station_list[i][j] == start:
                        path_list.append({"station":station_list[i][j],"before":station_list[i][j],"line":line_list[i]})

            while finish_flag == 0:
                for i in range(len(station_list)):
                    for j in range(len(station_list[i])):
                        if station_list[i][j] == search_station[0]:
                            if j == 0:
                                if len(set(check_station) & set([station_list[i][j+1]])) == 0:
                                    path_list.append({"station":station_list[i][j+1],"before":station_list[i][j],"line":line_list[i]})
                                    search_station.append(station_list[i][j+1])
                            if j == len(station_list[i])-1:
                                if len(set(check_station) & set([station_list[i][j-1]])) == 0:
                                    path_list.append({"station":station_list[i][j-1],"before":station_list[i][j],"line":line_list[i]})
                                    search_station.append(station_list[i][j-1])
                            if 0 < j and j < len(station_list[i])-1:
                                if len(set(check_station) & set([station_list[i][j-1]])) == 0:
                                    path_list.append({"station":station_list[i][j-1],"before":station_list[i][j],"line":line_list[i]})
                                    search_station.append(station_list[i][j-1])
                                if len(set(check_station) & set([station_list[i][j+1]])) == 0:
                                    path_list.append({"station":station_list[i][j+1],"before":station_list[i][j],"line":line_list[i]})
                                    search_station.append(station_list[i][j+1])

                check_station.append(search_station[0])
                search_index = 1
                while True:
                    if len(set([search_station[search_index]]) & set(check_station)) == 0:
                        search_station = search_station[search_index:]
                        break
                    else:
                        search_index += 1
                if search_station[0] == end:
                    finish_flag = 1
            return path_list


                                
        def decide_path(path_list,start,end):
            index = 0
            check_station = end
            path = []
            min_path = []
            while check_station != start:
                for i in range(len(path_list)):
                    if path_list[i]["station"] == check_station:
                        path.append(path_list[i]["station"])
                        path.append(u"\u2B07")
                        path.append(u"\u3016" + path_list[i]["line"] + u"\u3017")
                        path.append(u"\u2B07")
                        check_station = path_list[i]["before"]
            path.append(start)
            for p in reversed(path):
                min_path.append(p)
            
            return min_path

        def path_result(start_station,end_station):#探索した経路結果を返す
            if start_station == end_station:
                return []
            else:
                station_list,line_list = make_station_list()#線ごとに駅名をリストとして保存
                path_list = search_path(station_list,line_list,start_station,end_station)#ダイクストラ法で経路を探す
                min_path = decide_path(path_list,start_station,end_station)#最短の経路結果を返す
                #logging.info("============= say ==============")
                return min_path
 
        
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        self.response.out.write("""
                                <html>
                                  <head>
                                    <title>
                                      RESULT
                                    </title>
                                  <head>
                                  <body>
                                    Navigating Transit<br><br>
                                    ==============<br>
                                    Shortest route<br>
                                    ==============<br>
                                """)
        output = path_result(self.request.get("start_station"),self.request.get("end_station"))

        path = jinja2.Template(  # Jinjaのテンプレートエンジンを使ってHTMLを作成
        '''
        {% for min_path in output %}
          {{min_path}}<br>        
        {% endfor %}
        ''')
    
        self.response.out.write(path.render(output=output))
        self.response.out.write("""
                                  </body>
                                </html>
                                """
                                )


        
app = webapp2.WSGIApplication([("/", MainPage),
                               ("/input1", AlternateWordsPage),
                               ("/input2", TransferGuidePage),
                               ("/output1", Result_AlternateWordsPage),
                               ("/output2", Result_TransferGuidePage)],
                              debug=True)

