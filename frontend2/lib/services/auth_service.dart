import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/session_manager.dart';

class AuthService {
  // API base URL
  static const String baseUrl =
      'http://localhost:8000/api/v1'; // Using localhost
  // static const String baseUrl = 'http://10.0.2.2:8000/api/v1'; // For Android emulator
  // static const String baseUrl = 'http://192.168.223.18:8000/api/v1'; // Using actual IP address
  // static const String baseUrl = 'https://your-production-api.com/api/v1'; // For production

  // Session manager instance
  final SessionManager _sessionManager = SessionManager();

  // Register a new user
  Future<Map<String, dynamic>> register({
    required String username,
    required String email,
    required String password,
    required String fullName,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
        'full_name': fullName,
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      final data = jsonDecode(response.body);
      // Save user session
      await _sessionManager.saveUserSession(
        userId: data['id'],
        username: data['username'],
        email: data['email'],
        fullName: data['full_name'],
        accessToken: data['access_token'],
        refreshToken: data['refresh_token'],
      );
      return data;
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Registration failed');
    }
  }

  // Login with email and password
  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      // Get user info after successful login
      final userInfo = await getCurrentUser();

      // Save user session with user info from /me endpoint
      await _sessionManager.saveUserSession(
        userId: userInfo['id'],
        username: userInfo['username'],
        email: userInfo['email'],
        fullName: userInfo['full_name'],
        accessToken: data['access_token'],
        refreshToken: data['refresh_token'],
      );

      return {...data, ...userInfo};
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Login failed');
    }
  }

  // Login with Google
  Future<Map<String, dynamic>> loginWithGoogle(String idToken) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/google'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'id_token': idToken,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      // Get user info after successful login
      final userInfo = await getCurrentUser();

      // Save user session with user info from /me endpoint
      await _sessionManager.saveUserSession(
        userId: userInfo['id'],
        username: userInfo['username'],
        email: userInfo['email'],
        fullName: userInfo['full_name'],
        accessToken: data['access_token'],
        refreshToken: data['refresh_token'],
      );

      return {...data, ...userInfo};
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Google login failed');
    }
  }

  // Get current user info
  Future<Map<String, dynamic>> getCurrentUser() async {
    final token = await getAccessToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final response = await http.get(
      Uri.parse('$baseUrl/auth/me'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      // Try to refresh token if unauthorized
      if (response.statusCode == 401) {
        final refreshed = await refreshToken();
        if (refreshed) {
          return getCurrentUser();
        }
      }
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to get user info');
    }
  }

  // Refresh token
  Future<bool> refreshToken() async {
    final refreshToken = await _sessionManager.getRefreshToken();

    if (refreshToken == null) {
      return false;
    }

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/refresh'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'refresh_token': refreshToken,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await _sessionManager.updateAccessToken(data['access_token']);
        await _sessionManager.updateRefreshToken(data['refresh_token']);
        return true;
      } else {
        // Clear tokens if refresh fails
        await logout();
        return false;
      }
    } catch (e) {
      await logout();
      return false;
    }
  }

  // Logout - clear session
  Future<void> logout() async {
    await _sessionManager.clearSession();
  }

  // Change password
  Future<bool> changePassword(
      String currentPassword, String newPassword) async {
    final token = await getAccessToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final response = await http.post(
      Uri.parse('$baseUrl/auth/change-password'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'current_password': currentPassword,
        'new_password': newPassword,
      }),
    );

    if (response.statusCode == 200) {
      return true;
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to change password');
    }
  }

  // Request password reset
  Future<bool> forgotPassword(String email) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/forgot-password'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
      }),
    );

    return response.statusCode == 200;
  }

  // Reset password with token
  Future<bool> resetPassword(String token, String email, String newPassword) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/reset-password'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'token': token,
        'email': email,
        'new_password': newPassword,
      }),
    );

    return response.statusCode == 200;
  }
  
  // Verify email with code
  Future<bool> verifyEmail(String email, String code) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/verify-email'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'code': code,
      }),
    );

    if (response.statusCode == 200) {
      return true;
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Email verification failed');
    }
  }

  // Get access token from session manager
  Future<String?> getAccessToken() async {
    return await _sessionManager.getAccessToken();
  }

  // Check if user is logged in
  Future<bool> isLoggedIn() async {
    return await _sessionManager.isLoggedIn();
  }

  // Get current user data
  Future<Map<String, dynamic>> getUserData() async {
    return await _sessionManager.getUserData();
  }
}
