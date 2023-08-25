//import 'dart:async';
import 'dart:convert';

//import 'dart:io';
import 'package:flutter/material.dart';
// import 'package:flutter_webview_pro/platform_interface.dart';
//import 'package:rentomat/models/detalji_ugovora.dart';
import 'package:http/http.dart' as http;
//import 'package:url_launcher/url_launcher.dart';
import 'package:rentomat/pages/vracanje/vracanje_sugestije.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';

const String _url =
    'https://selfcar.naisrobotics.com/web#action=624&active_id=7&cids=1&menu_id=251';
// import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';
// import 'package:pdf/pdf.dart';
// import 'package:image/image.dart';

Future ugovor(resrvation_number) async {
  //print(resrvation_number);

  var headers = {
    'Content-Type': 'text/html',
  };

  var data = '{"username":"odoo@irvas.rs", "password":"irvasadm"}';
  print(data);

  var url_token = Uri.parse('http://23.88.98.237:8069/api/auth/get_tokens');
  var res = await http.post(url_token, headers: headers, body: data);
  print(res.statusCode);
  if (res.statusCode != 200)
    throw Exception('http.get error: statusCode= ${res.statusCode}');
  var data_res = jsonDecode(res.body);

  var token = data_res["access_token"];
  print(token);
  print(token);
  //var token = await storage.read(key: "token");
  print(token);

  var url = Uri.parse(
      "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code','=','$resrvation_number')]");
  //var url = Uri.parse("http://23.88.98.237:8069/api/car.rental.contract?filters=[('state','=','reserved')]");

  var requestHeaders = {
    'Content-Type': 'application/json',
    'Access-Token': '$token',
  };

  final response = await http.get(url, headers: requestHeaders);

  //final parsedJson = jsonDecode(response.body.toString());
  //print(response.statusCode);
  if (response.statusCode == 200) {
    print(response.body);

    var data_res1 = jsonDecode(response.body);

    final id_ugovora = data_res1['results'][0]["id"];
    print(id_ugovora);

    var url_pdf = Uri.parse(
        "http://23.88.98.237:8069/api/report/get_pdf?report_name=fleet_rent.report_fleet_rent_pdf&ids=%5B$id_ugovora%5D");
    var requestHeaders_pdf = {
      'accept': '*/*',
      'Access-Token': '$token',
    };
    final response_pdf = await http.get(url_pdf, headers: requestHeaders_pdf);
    var base64_temp_pdf = response_pdf.body.toString();
    var base64_pdf = base64_temp_pdf.substring(1);
    base64_pdf = base64_pdf.substring(0, base64_pdf.length - 1);
    var final_data_64_pdf = base64_pdf.replaceAll(r'\n', r"");
    //var final_data_pdf = base64Decode(final_data_64_pdf);

    print(final_data_64_pdf);

    //return (data_res1['results'][0]["id"] ?? '32132');
    return 'Svidetalji.fromJson(parsedJson)';
  } else {
    throw Exception('Ugovor ne postoji');
  }
}

// loadPDF(ug_id) async {
//   try {
//     var token = '3232131';

//     //await file.writeAsBytes(final_data.buffer.asUint8List());
//   } catch (Exc) {
//     print(Exc);
//   }
// }

// import 'package:cheapcarhire/api/access_token.dart';

// void main() {
//   runApp(
//     MaterialApp(
//       theme: ThemeData(useMaterial3: true),
//       home: WebViewApp(),
//     ),
//   );
// }

// void _no_damage() {
//   MaterialPageRoute(builder: (context) => Preuzimanje_home());
// }

// void _with_damage() async {
//   if (!await launch(_url)) throw 'Could not launch $_url';
// }

class vracanje_ocena extends StatefulWidget {
  final String text;
  const vracanje_ocena({Key? key, required this.text}) : super(key: key);

  @override
  State<vracanje_ocena> createState() => _vracanje_ocenaState();
}

class _vracanje_ocenaState extends State<vracanje_ocena> {
  //final token = storage.read(key: "token");

  @override
  void initState() {
    super.initState();
    ugovor(widget.text);
  }

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
                SizedBox(height: 100),
                Text(
                  'Ocena usluge/Rate',
                  style: TextStyle(
                    // styling the text
                    fontSize: 15.0, //the size of the text
                    fontWeight: FontWeight.bold, // font weight
                    //color: Color(0xff4169e1)
                  ),
                ),
                SizedBox(height: 120),
                RatingBar.builder(
                  initialRating: 0,
                  minRating: 1,
                  direction: Axis.horizontal,
                  allowHalfRating: true,
                  itemCount: 5,
                  itemPadding: EdgeInsets.symmetric(horizontal: 4.0),
                  itemBuilder: (context, _) => Icon(
                    Icons.star,
                    color: Colors.amber,
                  ),
                  onRatingUpdate: (rating) {
                    print(rating);
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (_) => vracanje_sugestije(
                                  text: '33',
                                )));
                  },
                ),
                // GestureDetector(
                //   onTap: _no_damage,
                //   child: Container(
                //     width: MediaQuery.of(context).size.width * 0.95,
                //     //height: MediaQuery.of(context).size.height * 0.2,
                //     //color: Color.fromARGB(3, 255, 255, 255),
                //     margin: const EdgeInsets.all(15.0),
                //     padding: const EdgeInsets.all(3.0),
                //     decoration: BoxDecoration(
                //         border: Border.all(
                //             color: const Color.fromARGB(255, 249, 133, 6))),
                //     child: Column(
                //       children: [
                //         Text(
                //           'Bez oštećenja/Bez kazni',
                //           style: TextStyle(
                //             // styling the text
                //             fontSize: 30.0, //the size of the text
                //             fontWeight: FontWeight.bold, // font weight
                //             //color: Color(0xff4169e1)
                //           ),
                //         ),
                //         Text(
                //           'No damages/No penalties',
                //           style: TextStyle(
                //             // styling the text
                //             fontSize: 30.0, //the size of the text
                //             fontWeight: FontWeight.bold, // font weight
                //             //color: Color(0xff4169e1)
                //           ),
                //         ),
                //       ],
                //     ),
                //   ),
                // ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
