#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import cgi

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        self.response.out.write("""
                                <html>
                                  <head>
                                    <title>
                                      input
                                    </title>
                                  <head>
                                  <body>
                                    <form action="/result" method="post">
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


class ResultPage(webapp2.RequestHandler):

    
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
                                      output
                                    </title>
                                  <head>
                                  <body>
                                    The two words you inputed are ...<br>
                                """)
        output = alternate_words(self.request.get("input1"),self.request.get("input2"))
        self.response.out.write(output)
        self.response.out.write("""<br> .... !?!?!?
                                  </body>
                                </html>
                                """
                                )

app = webapp2.WSGIApplication([("/", MainPage),
                               ("/result", ResultPage)],
                              debug=True)

