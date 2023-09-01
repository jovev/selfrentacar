import 'package:flutter/material.dart';
//import 'package:rentomat/pages/home.dart';
//import 'package:flag/flag.dart';
import 'package:rentomat/pages/preuzimanje/preuzimanje_home.dart';
import 'package:rentomat/pages/vracanje/vracanje_home.dart';
import 'package:url_launcher/url_launcher.dart';
//import 'package:animated_background/animated_background.dart';

void main() {
  runApp(const LandingPage());
}







class LandingPage extends StatefulWidget {
  const LandingPage({super.key});

  @override
  State<LandingPage> createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage> {
   @override
    void initState() {
      super.initState();
      
    }




  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      //title: 'Flutter Demo',
      // theme: new ThemeData(
      //     scaffoldBackgroundColor: Color.fromARGB(255, 224, 224, 224)),
      home: const MyHomePage(title: 'Rentomat'),
    );
  }
}

_launchURL() async {
  final Uri url = Uri.parse('https://cheapcarhire.rent/');
  if (!await launchUrl(url)) {
    throw Exception('Could not launch $url');
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage>
    with SingleTickerProviderStateMixin {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        //crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => vracanje_home()),
              );
            },
            child: Container(
              width: MediaQuery.of(context).size.width * 1,
              height: MediaQuery.of(context).size.height * 0.2,
              //color: Color.fromARGB(3, 255, 255, 255),
              margin: const EdgeInsets.all(15.0),
              padding: const EdgeInsets.all(3.0),
              decoration: BoxDecoration(
                  border: Border.all(
                      color: const Color.fromARGB(255, 249, 133, 6))),
              child: Image.asset('assets/img/drop.jpg'),
            ),
          ),
          GestureDetector(
            onTap: _launchURL,
            child: Container(
              width: MediaQuery.of(context).size.width * 0.95,
              height: MediaQuery.of(context).size.height * 0.25,
              margin: const EdgeInsets.all(15.0),
              padding: const EdgeInsets.all(113.0),
              decoration: BoxDecoration(
                  border: Border.all(
                      color: const Color.fromARGB(255, 249, 133, 6))),
              child: Column(
                children: [
                  Image.asset('assets/img/logooo.png'),
                  Text('WEB REZERVACIJA', style: TextStyle(
                            // styling the text
                            fontSize: 45.0, //the size of the text
                            fontWeight: FontWeight.bold, // font weight
                            //color: Color(0xff4169e1)
                          ),),
                  Text('www.cheapcarhire.rent', style: TextStyle(
                            // styling the text
                            fontSize: 45.0, //the size of the text
                            fontWeight: FontWeight.bold, // font weight
                            //color: Color(0xff4169e1)
                          ),)
                ],
              ),
            ),
          ),
          GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => Preuzimanje_home()),
              );
            },
            child: Container(
              width: MediaQuery.of(context).size.width * 0.95,
              height: MediaQuery.of(context).size.height * 0.2,
              margin: const EdgeInsets.all(15.0),
              padding: const EdgeInsets.all(3.0),
              decoration: BoxDecoration(
                  border: Border.all(
                      color: const Color.fromARGB(255, 249, 133, 6))),
              child: Image.asset('assets/img/take.png'),
            ),
          ),
          SizedBox(height: 80),

          // Container(
          //   //color: Colors.black,
          //   child: Row(
          //     children: [
          //       Expanded(
          //         child: Column(
          //           children: [
          //             Flag.fromCode(
          //               FlagsCode.RS,
          //               height: 30,
          //             ),
          //             Padding(
          //               padding: const EdgeInsets.all(28.0),
          //               child: ElevatedButton(
          //                 // style: ElevatedButton.styleFrom(
          //                 //   padding: const EdgeInsets.all(10),
          //                 //   primary:
          //                 //       Theme.of(context).secondaryHeaderColor,
          //                 // ),
          //                 //style: raisedButtonStyle,
          //                 onPressed: () {
          //                   Navigator.push(
          //                     context,
          //                     MaterialPageRoute(
          //                         builder: (context) => Home()),
          //                   );
          //                 },
          //                 child: Text('SRPSKI'),
          //               ),
          //             ),
          //           ],
          //         ),
          //       ),
          //       Expanded(
          //         child: Column(
          //           children: [
          //             Flag.fromCode(
          //               FlagsCode.GB_ENG,
          //               height: 30,
          //             ),
          //             Padding(
          //               padding: const EdgeInsets.all(28.0),
          //               child: ElevatedButton(
          //                 //style: raisedButtonStyle,
          //                 onPressed: () {
          //                   Navigator.push(
          //                     context,
          //                     MaterialPageRoute(
          //                         builder: (context) => Home()),
          //                   );
          //                 },
          //                 child: Text('ENGLISH'),
          //               ),
          //             ),
          //           ],
          //         ),
          //       )
          //     ],
          //   ),
          // )
        ],
      ),
    );
  }
}
