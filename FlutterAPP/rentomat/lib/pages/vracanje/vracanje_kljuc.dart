import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
//import 'package:rentomat/pages/vracanje/vracanje_potvrda.dart';
//import 'package:flutter_libserialport/flutter_libserialport.dart';


//import 'dart:convert' as convert;

//import 'package:http/http.dart' as http;



class vracanje_kljuc extends StatefulWidget {
  final String text;
  const vracanje_kljuc({Key? key, required this.text}) : super(key: key);

  @override
  State<vracanje_kljuc> createState() => _vracanje_kljucState();
}

class _vracanje_kljucState extends State<vracanje_kljuc> {
  //final token = storage.read(key: "token");
  var availablePorts = [];



  @override
  void initState() {
    super.initState();
    //ugovor(widget.text);
    //initPorts();


  

    
  }


  
  Future<void> httpReq() async {
    // List<String> availablePorts = SerialPort.availablePorts;  
    // //SerialPortParity(0);

    
    // var availablePort = availablePorts[0];
    // SerialPort port = SerialPort(availablePort);
    // print(availablePort);

   final queryParameters = {
    'pos': '2'
  };
    var url = Uri.http('127.0.0.0:5000', '/EMPTY',queryParameters);

    var response = await http.get(url);

    print(response.body);

    // if (response.statusCode == 200) {
    //   var jsonResponse = convert.jsonDecode(response.body);

    //   print(jsonResponse);

    // } else {
    //   print('Request failed with status');
    // }

    
  }




initPorts() async {
    

    // List<String> availablePorts = SerialPort.availablePorts;  
    // //SerialPortParity(0);
    // var availablePort = availablePorts[0];
    // SerialPort port = SerialPort(availablePort);

    // if(port.isOpen) {

    // } else {
    //   port.openReadWrite();
    // }
    
    

    // final reader = SerialPortReader(port);
   


    //     Stream<String> upcommingData = reader.stream.map((data) {
    //     return String.fromCharCodes(data);
    //   });
    

    // upcommingData.listen((data) {
    //   print(data.runtimeType);
    //   print(data);
    //     // print('from upcomming');
    //     // print(port1.isOpen);
    // });

   
  }



  Uint8List _stringToUinit8List(String data) {
    List<int> codeUnits = data.codeUnits;
    Uint8List uinit8list = Uint8List.fromList(codeUnits);
    return uinit8list;
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

                Container(
                    height: MediaQuery.of(context).size.height * 0.3,
                    child: Image.asset('assets/img/drop_off_key.jpg')),

                SizedBox(height: 20),
                GestureDetector(
                  onTap: () {
                    initPorts();

                    // Navigator.push(
                    //     context,
                    //     MaterialPageRoute(
                    //         builder: (_) => vracanje_potvrda(
                    //               text: '33',
                    //             )));
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
                          'Drop off the key',
                          style: TextStyle(
                            // styling the text
                            fontSize: 15.0, //the size of the text
                            fontWeight: FontWeight.bold, // font weight
                            //color: Color(0xff4169e1)
                          ),
                        ),
                        Text(
                          'Vrati ključ',
                          style: TextStyle(
                            // styling the text
                            fontSize: 15.0, //the size of the text
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
                    httpReq();

                    // Navigator.push(
                    //     context,
                    //     MaterialPageRoute(
                    //         builder: (_) => vracanje_potvrda(
                    //               text: '33',
                    //             )));
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
                          'Zatvori port',
                          style: TextStyle(
                            // styling the text
                            fontSize: 15.0, //the size of the text
                            fontWeight: FontWeight.bold, // font weight
                            //color: Color(0xff4169e1)
                          ),
                        ),
                  
                      ],
                    ),
                  ),
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
