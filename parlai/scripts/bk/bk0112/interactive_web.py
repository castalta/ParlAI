#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Talk with a model using a web UI.
## Examples
```shell
parlai interactive_web -mf "zoo:tutorial_transformer_generator/model"
```
"""


from http.server import BaseHTTPRequestHandler, HTTPServer
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
from parlai.core.script import ParlaiScript, register_script
import parlai.utils.logging as logging

import json
import time

HOST_NAME = 'localhost'
PORT = 8080

SHARED: Dict[Any, Any] = {}
STYLE_SHEET = "https://altavista21.com/my.css"
FONT_AWESOME = "https://altavista21.com/vue.js"
WEB_HTML = """
<html>
    <link rel="stylesheet" href={} media="screen"/>
    <script defer src={}></script>
    <head>
    <title> Alisa|English conversation practice with AI chat.</title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Cache-Control" content="no-cache">
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-186249509-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'UA-186249509-1');
    </script>
    </head>
    <body>
     <div style="text-align: center">
     <p><img class="spview" src="https://altavista21.com/img/alisa_sp.png"></p>
     <p><img class="pcview" src="https://altavista21.com/img/alisa.png"></p>
     </div>
        <div class="columns" style="height: 70%">
            <div class="column is-three-fifths is-offset-one-fifth">
                <div id="parent" class="hero-body scrollbar_none" style="overflow-wrap: normal;overflow-y:auto; height: calc(100% - 76px); padding-top: 1em; padding-bottom: 0;">
                        <div class="bubble04">
                          <p class="typewriter wordb">
                            Hi, Hello!
                          </p>
                        </div>
                </div>
                <div class="cp_iptxt">
                <form id = "interact">
                <table align="center" width="70%">
                <tr>
                <td><input class="ef" type="text" id="userIn" placeholder="Type in a message."></td>
                <td><input id="respond" type="image" src="https://altavista21.com/img/send_sp3.png" alt="send"></td>
                <span class="focus_line"></span>
                </tr>
                </table>
                </form>
                </div>
            </div>
        </div>
        <script>
             var keynum = 100;
             var speakerId = 0;
             var ptagId = 1000;
             function createChatRow(agent, text) {{
                var article = document.createElement("article");
                var div = document.createElement("div");
                
                if(agent === "Model"){{
                    div.className = "bubble04 wordb";
                }}else{{
                    div.className = "bubble03 wordb";
                }}
                
                var p = document.createElement("p");
                var paraText = document.createTextNode(text);
                if(agent === "Model"){{
                ptagId+=1;
                keynum+=1;
                speakerId+=1;
                var ptag = String(ptagId);
                p.id = "ptagId" + ptag;
                sessionStorage.setItem(keynum, text);
                var speaker = document.createElement("img");
                speaker.id = speakerId;
                speaker.src = "https://altavista21.com/img/speaker_off_pc.png";
                // speaker.alt = text;
                var spkid = String(speakerId);
                speaker.setAttribute("onclick", "speakerId"+ spkid +"()");
                }}
                div.appendChild(p);
                if(agent === "Model"){{
                    p.className = "wb";
                }}
                p.appendChild(paraText);
                article.appendChild(div);

                // buttons
                if(agent === "Model"){{
                var br = document.createElement("br");
                article.appendChild(br);
                article.appendChild(speaker);
                
                var tran = document.createElement("img");
                tran.src = "https://altavista21.com/img/translate.png";
                article.appendChild(tran);
                // var note = document.createElement("img");
                // note.src = "https://altavista21.com/img/note.png";
                // article.appendChild(note);
                var abc = sessionStorage.getItem(keynum);
                console.log("text id " + keynum),console.log(abc);
                console.log("sound id" + speaker.id);
                }}
                  //  base2 = '/"' + ptag + '/"';
                  // var str = document.getElementById('/"'+ptag+'/"').innerHTML;
                  // str = str.replace("i am","I am");
                  // document.getElementById('/"'+ptag+'/"').innerHTML = str;
               return article;
            }}
         document.getElementById("interact").addEventListener("submit", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;
                document.getElementById('userIn').value = "";
                if (text == ""){{
                    text = "....";
                }}
                
                    var usermessage = document.getElementById("parent");
                    usermessage.append(createChatRow("You", text));
                    usermessage.scrollTo(0, usermessage.scrollHeight);
                    // typing gif ani
                    var aityping = document.getElementById("parent");
                    var div = document.createElement("div");
                    div.className = "bubble04type";
                    var img0 = document.createElement("img");
                    var img = document.createElement("img");
                    var img1 = document.createElement("img");
                    img0.src = "https://altavista21.com/img/space.png";
                    img.src = "https://altavista21.com/img/Typing35_3.gif";
                    img1.src = "https://altavista21.com/img/space.png";
                    img.id = "typeId";
                    // img.className = "type";
                    aityping.append(div);
                    div.appendChild(img0);
                    div.appendChild(img);
                    div.appendChild(img1);
                    aityping.scrollTo(0, aityping.scrollHeight);
                fetch('/interact', {{
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    method: 'POST',
                    body: text
                }}).then(response=>response.json()).then(data=>{{
                    var parDiv = document.getElementById("parent");
                    // parDiv.append(createChatRow("You", text));
                    // Change info for Model response
                    div.remove();
                    img.remove();
                    
                    parDiv.append(createChatRow("Model", data.text));
                    parDiv.scrollTo(0, parDiv.scrollHeight);
                }})
            }});
            document.getElementById("interact").addEventListener("reset", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;
                document.getElementById('userIn').value = "";
                fetch('/reset', {{
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    method: 'POST',
                }}).then(response=>response.json()).then(data=>{{
                    var parDiv = document.getElementById("parent");
                    parDiv.innerHTML = '';
                    parDiv.scrollTo(0, parDiv.scrollHeight);
                }})
            }});
        </script>
    </body>
</html>
"""  # noqa: E501


class MyHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests.
    """

    def _interactive_running(self, opt, reply_text):
        reply = {'episode_done': False, 'text': reply_text}
        SHARED['agent'].observe(reply)
        model_res = SHARED['agent'].act()
        return model_res

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Handle POST request, especially replying to a chat message.
        """
        if self.path == '/interact':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            model_response = self._interactive_running(
                SHARED.get('opt'), body.decode('utf-8')
            )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            json_str = json.dumps(model_response)
            self.wfile.write(bytes(json_str, 'utf-8'))
        elif self.path == '/reset':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            SHARED['agent'].reset()
            self.wfile.write(bytes("{}", 'utf-8'))
        else:
            return self._respond({'status': 500})

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/favicon.ico': {'status': 202},  # Need for chrome
        }
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})

    def _handle_http(self, status_code, path, text=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME)
        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)


def setup_interweb_args(shared):
    """
    Build and parse CLI opts.
    """
    parser = setup_args()
    parser.description = 'Interactive chat with a model in a web browser'
    parser.add_argument('--port', type=int, default=PORT, help='Port to listen on.')
    parser.add_argument(
        '--host',
        default=HOST_NAME,
        type=str,
        help='Host from which allow requests, use 0.0.0.0 to allow all IPs',
    )
    return parser


def shutdown():
    global SHARED
    if 'server' in SHARED:
        SHARED['server'].shutdown()
    SHARED.clear()


def wait():
    global SHARED
    while not SHARED.get('ready'):
        time.sleep(0.01)


def interactive_web(opt):
    global SHARED

    opt['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(opt, requireModelExists=True)
    agent.opt.log()
    SHARED['opt'] = agent.opt
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])

    MyHandler.protocol_version = 'HTTP/1.0'
    httpd = HTTPServer((opt['host'], opt['port']), MyHandler)
    SHARED['server'] = httpd
    logging.info('http://{}:{}/'.format(opt['host'], opt['port']))

    try:
        SHARED['ready'] = True
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


@register_script('interactive_web', aliases=['iweb'], hidden=True)
class InteractiveWeb(ParlaiScript):
    @classmethod
    def setup_args(cls):
        return setup_interweb_args(SHARED)

    def run(self):
        return interactive_web(self.opt)


if __name__ == '__main__':
    InteractiveWeb.main()