import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/session_manager.dart';

class ApiService {
  // API base URL
  static const String baseUrl =
      'http://localhost:8000/api/v1'; // Using localhost
  // static const String baseUrl = 'http://10.0.2.2:8000/api/v1'; // For Android emulator
  // static const String baseUrl = 'http://192.168.223.18:8000/api/v1'; // Using actual IP address
  // static const String baseUrl = 'https://your-production-api.com/api/v1'; // For production

  // Session manager instance
  final SessionManager _sessionManager = SessionManager();

  // Headers with authentication token
  Future<Map<String, String>> _getAuthHeaders() async {
    final token = await _sessionManager.getAccessToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  // GET request
  Future<dynamic> get(String endpoint) async {
    final headers = await _getAuthHeaders();
    final response = await http.get(
      Uri.parse('$baseUrl/$endpoint'),
      headers: headers,
    );

    return _handleResponse(response);
  }

  // POST request
  Future<dynamic> post(String endpoint, Map<String, dynamic> data) async {
    final headers = await _getAuthHeaders();
    final response = await http.post(
      Uri.parse('$baseUrl/$endpoint'),
      headers: headers,
      body: jsonEncode(data),
    );

    return _handleResponse(response);
  }

  // PUT request
  Future<dynamic> put(String endpoint, Map<String, dynamic> data) async {
    final headers = await _getAuthHeaders();
    final response = await http.put(
      Uri.parse('$baseUrl/$endpoint'),
      headers: headers,
      body: jsonEncode(data),
    );

    return _handleResponse(response);
  }

  // PATCH request
  Future<dynamic> patch(String endpoint, Map<String, dynamic> data) async {
    final headers = await _getAuthHeaders();
    final response = await http.patch(
      Uri.parse('$baseUrl/$endpoint'),
      headers: headers,
      body: jsonEncode(data),
    );

    return _handleResponse(response);
  }

  // DELETE request
  Future<dynamic> delete(String endpoint) async {
    final headers = await _getAuthHeaders();
    final response = await http.delete(
      Uri.parse('$baseUrl/$endpoint'),
      headers: headers,
    );

    return _handleResponse(response);
  }

  // Handle HTTP response
  dynamic _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return {};
      return jsonDecode(response.body);
    } else {
      // Try to parse error message
      try {
        final errorData = jsonDecode(response.body);
        throw Exception(errorData['detail'] ??
            'Request failed with status: ${response.statusCode}');
      } catch (e) {
        throw Exception('Request failed with status: ${response.statusCode}');
      }
    }
  }

  // Upload file
  Future<dynamic> uploadFile(
      String endpoint, String filePath, String fieldName) async {
    final token = await _sessionManager.getAccessToken();
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/$endpoint'),
    );

    // Add authorization header if token exists
    if (token != null) {
      request.headers['Authorization'] = 'Bearer $token';
    }

    // Add file to request
    request.files.add(await http.MultipartFile.fromPath(fieldName, filePath));

    // Send request
    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    return _handleResponse(response);
  }
}
