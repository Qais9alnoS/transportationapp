import 'package:flutter/material.dart';
import '../services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();
  bool _isLoading = false;
  String? _error;
  Map<String, dynamic>? _currentUser;
  bool _isLoggedIn = false;

  // Getters
  bool get isLoading => _isLoading;
  String? get error => _error;
  Map<String, dynamic>? get currentUser => _currentUser;
  bool get isLoggedIn => _isLoggedIn;

  // Constructor - check if user is already logged in
  AuthProvider() {
    _checkLoginStatus();
  }

  // Check if user is logged in
  Future<void> _checkLoginStatus() async {
    _setLoading(true);
    try {
      _isLoggedIn = await _authService.isLoggedIn();
      if (_isLoggedIn) {
        await _fetchCurrentUser();
      }
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Fetch current user data
  Future<void> _fetchCurrentUser() async {
    try {
      _currentUser = await _authService.getCurrentUser();
      notifyListeners();
    } catch (e) {
      _setError(e.toString());
    }
  }

  // Register
  Future<bool> register({
    required String username,
    required String email,
    required String password,
    required String fullName,
  }) async {
    _setLoading(true);
    _clearError();

    try {
      await _authService.register(
        username: username,
        email: email,
        password: password,
        fullName: fullName,
      );
      _isLoggedIn = true;
      await _fetchCurrentUser();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Login
  Future<bool> login(String email, String password) async {
    _setLoading(true);
    _clearError();

    try {
      await _authService.login(email, password);
      _isLoggedIn = true;
      await _fetchCurrentUser();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Login with Google
  Future<bool> loginWithGoogle(String idToken) async {
    _setLoading(true);
    _clearError();

    try {
      await _authService.loginWithGoogle(idToken);
      _isLoggedIn = true;
      await _fetchCurrentUser();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Logout
  Future<void> logout() async {
    _setLoading(true);
    _clearError();

    try {
      await _authService.logout();
      _isLoggedIn = false;
      _currentUser = null;
      notifyListeners();
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Forgot password
  Future<bool> forgotPassword(String email) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.forgotPassword(email);
      return result;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Verify email
  Future<bool> verifyEmail(String email, String code) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.verifyEmail(email, code);
      return result;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Reset password
  Future<bool> resetPassword(String token, String email, String newPassword) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.resetPassword(token, email, newPassword);
      return result;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Change password
  Future<bool> changePassword(
      String currentPassword, String newPassword) async {
    _setLoading(true);
    _clearError();

    try {
      final result =
          await _authService.changePassword(currentPassword, newPassword);
      return result;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Helper methods
  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }

  void _setError(String error) {
    _error = error;
    notifyListeners();
  }

  void _clearError() {
    _error = null;
    notifyListeners();
  }
}
