import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'screens/login_screen/login_screen.dart';
import 'screens/map_screen.dart';
import 'utils/constants.dart';
import 'utils/auth_guard.dart';
import 'providers/auth_provider.dart';
import 'providers/loading_provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => LoadingProvider()),
      ],
      child: MaterialApp(
        title: 'Login App',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          scaffoldBackgroundColor: kBackgroundColor,
          fontFamily: 'Cairo',
          textTheme: Theme.of(context).textTheme.apply(
                bodyColor: kPrimaryColor,
              ),
          textSelectionTheme: const TextSelectionThemeData(
            cursorColor: Color(0xFF06332E),
            selectionColor: Color(0x8006332E),
            selectionHandleColor: Color(0xFF06332E),
          ),
        ),
        home: const LoginScreen(),
        routes: {
          '/map': (context) => const AuthGuard(child: MapScreen()),
        },
      ),
    );
  }
}
