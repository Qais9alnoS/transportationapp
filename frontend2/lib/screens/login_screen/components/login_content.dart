import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:ionicons/ionicons.dart';
import 'package:login_screen/utils/helper_functions.dart';
import 'package:provider/provider.dart';
import '../../../providers/auth_provider.dart';
import '../animations/change_screen_animation.dart';
import 'bottom_text.dart';
import 'top_text.dart';
import '../verify_email_screen.dart';
import '../forgot_password_screen.dart';

enum Screens {
  createAccount,
  welcomeBack,
}

class LoginContent extends StatefulWidget {
  const LoginContent({Key? key}) : super(key: key);

  @override
  State<LoginContent> createState() => _LoginContentState();
}

class _LoginContentState extends State<LoginContent>
    with TickerProviderStateMixin {
  // Controllers for login fields
  final TextEditingController loginEmailController = TextEditingController();
  final TextEditingController loginPasswordController = TextEditingController();
  // Error messages for login fields
  String? loginEmailError;
  String? loginPasswordError;

  // Password visibility state
  bool _loginPasswordVisible = false;
  bool _signUpPasswordVisible = false;

  // Controllers for sign up fields
  final TextEditingController signUpNameController = TextEditingController();
  final TextEditingController signUpEmailController = TextEditingController();
  final TextEditingController signUpPasswordController =
      TextEditingController();
  // Error messages for sign up fields
  String? signUpNameError;
  String? signUpEmailError;
  String? signUpPasswordError;

  late final List<Widget> createAccountContent;
  late final List<Widget> loginContent;

  Widget inputField({
    required String hint,
    required IconData iconData,
    required TextEditingController controller,
    String? errorText,
    bool obscureText = false,
    VoidCallback? onToggleObscure,
    bool? isObscured,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 8),
      child: SizedBox(
        height: 48,
        child: Material(
          elevation: 4,
          shadowColor: Colors.black12,
          color: Colors.transparent,
          borderRadius: BorderRadius.circular(28),
          child: TextField(
            controller: controller,
            obscureText: obscureText && (isObscured ?? true),
            textAlignVertical: TextAlignVertical.center,
            style: const TextStyle(
              fontFamily: 'Montserrat',
              fontWeight: FontWeight.w500,
              color: Color(0xFF06332E),
            ),
            decoration: InputDecoration(
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(28),
                borderSide: BorderSide.none,
              ),
              filled: true,
              fillColor: Color(0xFFF5E9D0), // light beige
              hintText: errorText ?? hint,
              hintStyle: TextStyle(
                color: errorText != null ? Colors.red : Color(0xFF8F8262),
                fontFamily: 'Montserrat',
                fontWeight: FontWeight.w400,
              ),
              prefixIcon: Icon(iconData, color: Color(0xFF8F8262)),
              contentPadding: const EdgeInsets.only(left: 16, top: 10, bottom: 0, right: 16),
              suffixIcon: obscureText
                  ? IconButton(
                      icon: Icon(
                        (isObscured ?? true)
                            ? Icons.visibility
                            : Icons.visibility_off,
                        color: Color(0xFF8F8262),
                      ),
                      onPressed: onToggleObscure,
                    )
                  : null,
            ),
          ),
        ),
      ),
    );
  }

  bool isValidEmail(String email) {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email);
  }

  bool isValidPassword(String password) {
    return password.length >= 8 && !password.contains(' ');
  }

  Widget loginButton(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 12),
      child: SizedBox(
        height: 48,
        child: ElevatedButton(
          onPressed: () {
            // Prevent multiple button presses
            FocusScope.of(context).unfocus();
            final authProvider = Provider.of<AuthProvider>(context, listen: false);
            
            setState(() {
              if (title == 'Log In') {
                final trimmedLoginEmail = loginEmailController.text.trim();
                if (trimmedLoginEmail.isEmpty) {
                  loginEmailError = 'fill the field';
                  loginEmailController.clear();
                } else if (!isValidEmail(trimmedLoginEmail)) {
                  loginEmailError = 'invalid email';
                  loginEmailController.clear();
                } else {
                  loginEmailError = null;
                }

                if (loginPasswordController.text.isEmpty) {
                  loginPasswordError = 'fill the field';
                  loginPasswordController.clear();
                } else if (!isValidPassword(loginPasswordController.text)) {
                  loginPasswordError = 'invalid password';
                  loginPasswordController.clear();
                } else {
                  loginPasswordError = null;
                }

                if (loginEmailError == null && loginPasswordError == null) {
                  // Show loading indicator
                  showDialog(
                    context: context,
                    barrierDismissible: false,
                    builder: (context) => const Center(child: CircularProgressIndicator()),
                  );
                  
                  try {
                    // Call login without await
                    authProvider.login(
                      trimmedLoginEmail,
                      loginPasswordController.text,
                    ).then((success) {
                      // Close loading dialog
                      Navigator.of(context).pop();
                      
                      if (success) {
                        Navigator.of(context).pushReplacementNamed('/map');
                      } else {
                        // Show error message
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text(authProvider.error ?? 'Login failed')),
                        );
                      }
                    }).catchError((e) {
                      // Close loading dialog
                      Navigator.of(context).pop();
                      // Show error message
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text(e.toString())),
                      );
                    });
                  } catch (e) {
                    // This catch block will handle synchronous errors
                    // Close loading dialog
                    Navigator.of(context).pop();
                    // Show error message
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text(e.toString())),
                    );
                  }
                }
              } else {
                // Sign Up logic
                final fullName = signUpNameController.text.trim();
                if (fullName.isEmpty) {
                  signUpNameError = 'fill the field';
                  signUpNameController.clear();
                } else {
                  signUpNameError = null;
                }

                final trimmedSignUpEmail = signUpEmailController.text.trim();
                if (trimmedSignUpEmail.isEmpty) {
                  signUpEmailError = 'fill the field';
                  signUpEmailController.clear();
                } else if (!isValidEmail(trimmedSignUpEmail)) {
                  signUpEmailError = 'invalid email';
                  signUpEmailController.clear();
                } else {
                  signUpEmailError = null;
                }

                if (signUpPasswordController.text.isEmpty) {
                  signUpPasswordError = 'fill the field';
                  signUpPasswordController.clear();
                } else if (!isValidPassword(signUpPasswordController.text)) {
                  signUpPasswordError = 'invalid password';
                  signUpPasswordController.clear();
                } else {
                  signUpPasswordError = null;
                }

                if (signUpNameError == null &&
                    signUpEmailError == null &&
                    signUpPasswordError == null) {
                  
                  // Show loading indicator
                  showDialog(
                    context: context,
                    barrierDismissible: false,
                    builder: (context) => const Center(child: CircularProgressIndicator()),
                  );
                  
                  try {
                    // Generate a username from email (before @ symbol)
                    final username = trimmedSignUpEmail.split('@')[0];
                    
                    // Call register without await
                    authProvider.register(
                      username: username,
                      email: trimmedSignUpEmail,
                      password: signUpPasswordController.text,
                      fullName: fullName,
                    ).then((success) {
                      // Close loading dialog
                      Navigator.of(context).pop();
                      
                      if (success) {
                        Navigator.of(context).pushReplacement(
                          MaterialPageRoute(
                            builder: (context) => VerifyEmailScreen(email: trimmedSignUpEmail),
                          ),
                        );
                      } else {
                        // Show error message
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text(authProvider.error ?? 'Registration failed')),
                        );
                      }
                    }).catchError((e) {
                      // Close loading dialog
                      Navigator.of(context).pop();
                      // Show error message
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text(e.toString())),
                      );
                    });
                  } catch (e) {
                    // This catch block will handle synchronous errors
                    // Close loading dialog
                    Navigator.of(context).pop();
                    // Show error message
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text(e.toString())),
                    );
                  }
                }
              }
            });
          },
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 24),
            shape: const StadiumBorder(),
            backgroundColor: Colors.transparent,
            shadowColor: Colors.transparent,
            elevation: 0,
          ).copyWith(
            backgroundColor: MaterialStateProperty.all(Colors.transparent),
            elevation: MaterialStateProperty.all(0),
            shadowColor: MaterialStateProperty.all(Colors.transparent),
            padding: MaterialStateProperty.all(const EdgeInsets.symmetric(vertical: 0, horizontal: 0)),
            foregroundColor: MaterialStateProperty.all(Colors.transparent),
            surfaceTintColor: MaterialStateProperty.all(Colors.transparent),
            overlayColor: MaterialStateProperty.all(Colors.transparent),
          ),
          child: Ink(
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [
                  Color(0xFF06332E), // dark green
                  Color(0xFF0B664E), // subtle darker green
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(30),
            ),
            child: Container(
              alignment: Alignment.center,
              height: 48,
              child: Text(
                title,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFFF5E9D0), // beige
                  fontFamily: 'Montserrat',
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget orDivider() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 12),
      child: Row(
        children: [
          Expanded(
            child: Container(
              height: 1.2,
              color: const Color(0xFFC2B185),
            ),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 12),
            child: Text(
              'or',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: Color(0xFFC2B185),
                fontFamily: 'Montserrat',
              ),
            ),
          ),
          Expanded(
            child: Container(
              height: 1.2,
              color: const Color(0xFFC2B185),
            ),
          ),
        ],
      ),
    );
  }

  Widget socialLoginButtons() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SizedBox(
            width: 130,
            height: 42,
            child: ElevatedButton.icon(
              onPressed: () async {
                final authProvider = Provider.of<AuthProvider>(context, listen: false);
                
                // Show loading indicator
                showDialog(
                  context: context,
                  barrierDismissible: false,
                  builder: (context) => const Center(child: CircularProgressIndicator()),
                );
                
                try {
                  // TODO: Implement Google Sign-In to get idToken
                  // For now, we'll just show a message that this is not implemented
                  Navigator.of(context).pop(); // Close loading dialog
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Google login not implemented yet')),
                  );
                  
                  // When implemented, it would look like this:
                  // final googleSignIn = GoogleSignIn();
                  // final googleUser = await googleSignIn.signIn();
                  // final googleAuth = await googleUser?.authentication;
                  // final idToken = googleAuth?.idToken;
                  // 
                  // if (idToken != null) {
                  //   final success = await authProvider.loginWithGoogle(idToken);
                  //   if (success) {
                  //     Navigator.of(context).pushReplacementNamed('/map');
                  //   }
                  // }
                } catch (e) {
                  // Close loading dialog
                  Navigator.of(context).pop();
                  // Show error message
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text(e.toString())),
                  );
                }
              },
              icon: Image.asset(
                'assets/images/google.png',
                height: 20,
                width: 20,
              ),
              label: const Text(
                'Google',
                style: TextStyle(
                  color: Color(0xFF06332E),
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Montserrat',
                ),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFFF5E9D0), // light beige
                elevation: 1,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(28),
                  side: const BorderSide(color: Color(0xFFC2B185), width: 1),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 0),
              ),
            ),
          ),
          const SizedBox(width: 10),
          SizedBox(
            width: 130,
            height: 42,
            child: ElevatedButton.icon(
              onPressed: () {
                // TODO: Implement Facebook login
              },
              icon: Image.asset(
                'assets/images/facebook.png',
                height: 20,
                width: 20,
              ),
              label: const Text(
                'Facebook',
                style: TextStyle(
                  color: Color(0xFFF5E9D0),
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Montserrat',
                ),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF8F8262), // muted beige-brown
                elevation: 1,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(28),
                  side: const BorderSide(color: Color(0xFFC2B185), width: 1),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 0),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget forgotPassword() {
    return Padding(
      padding: const EdgeInsets.only(right: 24.0),
      child: Align(
        alignment: Alignment.centerRight,
        child: TextButton(
          onPressed: () {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => const ForgotPasswordScreen(),
              ),
            );
          },
          child: const Text(
            'Forgot Password?',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: Color(0xFF06332E),
            ),
          ),
        ),
      ),
    );
  }

  @override
  void initState() {
    super.initState();
    ChangeScreenAnimation.initialize(
      vsync: this,
      createAccountItems: 7, // 1 SizedBox + 3 fields + button + divider + social buttons
      loginItems: 7, // 1 SizedBox + 2 fields + button + forgotPassword + divider + social buttons
    );
  }

  @override
  void dispose() {
    loginEmailController.dispose();
    loginPasswordController.dispose();
    signUpNameController.dispose();
    signUpEmailController.dispose();
    signUpPasswordController.dispose();
    ChangeScreenAnimation.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final createAccountContent = [
      const SizedBox(height: 16),
      inputField(
          hint: 'Name',
          iconData: Ionicons.person_outline,
          controller: signUpNameController,
          errorText: signUpNameError),
      inputField(
          hint: 'Email',
          iconData: Ionicons.mail_outline,
          controller: signUpEmailController,
          errorText: signUpEmailError),
      inputField(
          hint: 'Password',
          iconData: Ionicons.lock_closed_outline,
          controller: signUpPasswordController,
          errorText: signUpPasswordError,
          obscureText: true,
          isObscured: !_signUpPasswordVisible,
          onToggleObscure: () {
            setState(() {
              _signUpPasswordVisible = !_signUpPasswordVisible;
            });
          }),
      loginButton('Sign Up'),
      orDivider(),
      socialLoginButtons(),
    ];

    final loginContent = [
      const SizedBox(height: 16),
      inputField(
          hint: 'Email',
          iconData: Ionicons.mail_outline,
          controller: loginEmailController,
          errorText: loginEmailError),
      inputField(
          hint: 'Password',
          iconData: Ionicons.lock_closed_outline,
          controller: loginPasswordController,
          errorText: loginPasswordError,
          obscureText: true,
          isObscured: !_loginPasswordVisible,
          onToggleObscure: () {
            setState(() {
              _loginPasswordVisible = !_loginPasswordVisible;
            });
          }),
      loginButton('Log In'),
      forgotPassword(),
      orDivider(),
      socialLoginButtons(),
    ];

    final animatedCreateAccountContent = [
      for (var i = 0; i < createAccountContent.length; i++)
        HelperFunctions.wrapWithAnimatedBuilder(
          animation: ChangeScreenAnimation.createAccountAnimations[i],
          child: createAccountContent[i],
        ),
    ];
    final animatedLoginContent = [
      for (var i = 0; i < loginContent.length; i++)
        HelperFunctions.wrapWithAnimatedBuilder(
          animation: ChangeScreenAnimation.loginAnimations[i],
          child: loginContent[i],
        ),
    ];

    return Center(
      child: ClipRRect(
        borderRadius: BorderRadius.circular(32),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 16, sigmaY: 16),
          child: Container(
            constraints: const BoxConstraints(
              minWidth: 350,
              maxWidth: 420,
              minHeight: 500,
              maxHeight: 650,
            ),
            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 32),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.18),
              borderRadius: BorderRadius.circular(32),
              border:
                  Border.all(color: Colors.white.withOpacity(0.3), width: 1.2),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const TopText(),
                Stack(
                  children: [
                    Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: animatedCreateAccountContent,
                    ),
                    Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: animatedLoginContent,
                    ),
                  ],
                ),
                const Align(
                  alignment: Alignment.bottomCenter,
                  child: Padding(
                    padding: EdgeInsets.only(bottom: 10),
                    child: BottomText(),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
