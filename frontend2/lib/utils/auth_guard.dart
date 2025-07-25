import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../screens/login_screen/login_screen.dart';

class AuthGuard extends StatelessWidget {
  final Widget child;

  const AuthGuard({Key? key, required this.child}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthProvider>(
      builder: (context, authProvider, _) {
        // Show loading indicator while checking login status
        if (authProvider.isLoading) {
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        // If not logged in, redirect to login screen
        if (!authProvider.isLoggedIn) {
          return const LoginScreen();
        }

        // If logged in, show the protected content
        return child;
      },
    );
  }
}

// Extension method for Navigator to push a protected route
extension AuthNavigator on NavigatorState {
  Future<T?> pushProtected<T extends Object?>(
    BuildContext context,
    Widget page, {
    bool replace = false,
  }) async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);

    if (!authProvider.isLoggedIn) {
      // If not logged in, redirect to login screen
      if (replace) {
        return pushReplacement(
            MaterialPageRoute(builder: (_) => const LoginScreen()));
      } else {
        return push(MaterialPageRoute(builder: (_) => const LoginScreen()));
      }
    } else {
      // If logged in, navigate to the requested page
      if (replace) {
        return pushReplacement(MaterialPageRoute(builder: (_) => page));
      } else {
        return push(MaterialPageRoute(builder: (_) => page));
      }
    }
  }
}
