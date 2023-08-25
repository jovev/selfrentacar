import 'dart:convert';
//import 'dart:html';

import 'package:flutter/material.dart';
//import 'package:flutter_secure_storage/flutter_secure_storage.dart';
//import 'package:rentomat/pages/preuzimanje/preuzimanje_ugovor.dart';
import 'package:http/http.dart' as http;
import 'package:rentomat/pages/preuzimanje/preuzimanje_ugovor.dart';
//import '../../main.dart';
import 'package:url_launcher/url_launcher.dart';

//final Uri _url = Uri.parse('https://flutter.dev');
_launchURL() async {
  final Uri url = Uri.parse(
      'https://selfcar.naisrobotics.com/web#id=38&cids=1&menu_id=251&action=625&model=fleet.rent&view_type=form');
  if (!await launchUrl(url)) {
    throw Exception('Could not launch $url');
  }
}

void main() {
  runApp(const Preuzimanje_home());
}

class Preuzimanje_home extends StatelessWidget {
  const Preuzimanje_home({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      //title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: const Color.fromARGB(255, 255, 255, 255)),
        useMaterial3: true,
      ),
      home: MyHomePage(title: 'Rentomat'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  TextEditingController textFieldController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          //mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            SizedBox(height: 20),
            Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                    height: MediaQuery.of(context).size.height * 0.1,
                    child: Image.asset('assets/img/logooo.png')),
                SizedBox(height: 20),
                Container(
                    height: MediaQuery.of(context).size.height * 0.5,
                    child: Image.asset('assets/img/qr_scan.jpg')),
                GestureDetector(
                  onTap: _launchURL,
                  child: Container(
                    width: MediaQuery.of(context).size.width * 0.95,
                    margin: const EdgeInsets.all(15.0),
                    padding: const EdgeInsets.all(3.0),
                    decoration: BoxDecoration(
                        border: Border.all(
                            color: const Color.fromARGB(255, 249, 133, 6))),
                    child: Column(
                      children: [
                        Text(
                          'Scan QR code ppp',
                          style: TextStyle(
                            // styling the text
                            fontSize: 45.0, //the size of the text
                            fontWeight: FontWeight.bold, // font weight
                            //color: Color(0xff4169e1)
                          ),
                        ),
                        Text(
                          'Skeniraj QR kod',
                          style: TextStyle(
                            // styling the text
                            fontSize: 45.0, //the size of the text
                            fontWeight: FontWeight.bold, // font weight
                            //color: Color(0xff4169e1)
                          ),
                        ),
                      ],
                    ),
                  ),
                ),


                GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => preuzimanje_ugovor(
                                text: '38',
                              )),
                    );
                  },
                  child: Container(
                    width: MediaQuery.of(context).size.width * 0.95,
                    //height: MediaQuery.of(context).size.height * 0.2,
                    //color: Color.fromARGB(3, 255, 255, 255),
                    margin: const EdgeInsets.all(15.0),
                    padding: const EdgeInsets.all(3.0),
                    decoration: BoxDecoration(
                        border: Border.all(
                            color: const Color.fromARGB(255, 249, 133, 6))),
                    child: Column(
                      children: [
                        Text(
                          'Preuzmi ugovor',
                          style: TextStyle(
                            // styling the text
                            fontSize: 45.0, //the size of the text
                            fontWeight: FontWeight.bold, // font weight
                            //color: Color(0xff4169e1)
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                Container(
                    child: Column(
                  children: [
                    SizedBox(
                      width: 400.0,
                      child: TextField(
                        controller: textFieldController,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: 'BAR code',
                        ),
                      ),
                    ),
                    // SizedBox(height: 40),
                    // ElevatedButton(
                    //   // style: ElevatedButton.styleFrom(
                    //   //   padding: const EdgeInsets.all(10),
                    //   //   primary:
                    //   //       Theme.of(context).secondaryHeaderColor,
                    //   // ),
                    //   //style: raisedButtonStyle,
                    //   onPressed: () {
                    //     Navigator.push(
                    //       context,
                    //       MaterialPageRoute(
                    //           builder: (context) => preuzimanje_ugovor(
                    //               text: textFieldController.text)),
                    //     );
                    //   },
                    //   child: Text('SKENIRAJ'),
                    // ),
                    // ElevatedButton(
                    //   onPressed: () => loadPDF("nekitekst"),
                    //   child: const Text('Submit'),
                    // ),
                  ],
                ))
              ],
            ),
          ],
        ),
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed: () {
      //     Navigator.push(
      //       context,
      //       MaterialPageRoute(builder: (context) => LandingPage()),
      //     );
      //   },
      //   tooltip: 'HOME',
      //   child: const Text('HOME'),
      // ),
    );
  }

  get_acces_token() async {
    var headers = {
      'Content-Type': 'text/html',
    };

    //print(username);
    //print(pass);
    //var data = '{"username":"$username", "password":"$pass"}';
    var data = '{"username":"odoo@irvas.rs", "password":"irvasadm"}';
    //var data = '{"username":$username, "password":$pass}';

    var url = Uri.parse('http://23.88.98.237:8069/api/auth/get_tokens');
    var res = await http.post(url, headers: headers, body: data);
    if (res.statusCode != 200) {
      throw Exception('http.get error: statusCode= ${res.statusCode}');
    } else {
      var data_res = jsonDecode(res.body);

      // var acc_token = data_res['access_token'];

      // print(data_res['access_token']);

      // var data_res = jsonDecode(res.body);
      //final storage = new FlutterSecureStorage();
      //await storage.write(key: "token", value: data_res["access_token"]);
      return data_res["access_token"];
    }
  }

  // loadPDF(ug_id) async {
  //   try {
  //     var token = get_acces_token();
  //     var url = Uri.parse(
  //         "http://23.88.98.237:8069/api/report/get_pdf?report_name=fleet_rent.report_fleet_rent_pdf&ids=%5B$ug_id%5D");
  //     var requestHeaders = {
  //       'accept': '*/*',
  //       'Access-Token': '$token',
  //     };
  //     final response = await http.get(url, headers: requestHeaders);
  //     var base64_temp = response.body.toString();
  //     var base64 = base64_temp.substring(1);
  //     base64 = base64.substring(0, base64.length - 1);
  //     var final_data_tmp = base64.replaceAll(r'\n', r"");
  //     var final_data = base64Decode(final_data_tmp);
  //     final dir_path =
  //         '/storage/emulated/0/Android/data/com.example.cheapcarhire/files';
  //     File file = new File("$dir_path/ugovor.pdf");
  //     await file.writeAsBytes(final_data.buffer.asUint8List());
  //     await OpenFilex.open("$dir_path/ugovor.pdf");
  //   } catch (Exc) {
  //     print(Exc);
  //   }
  // }
}
