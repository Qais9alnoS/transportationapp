import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'trip_rating_screen.dart';
import 'dart:ui';

class TripTrackingScreen extends StatelessWidget {
  const TripTrackingScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Static mock coordinates for demo
    final List<LatLng> mikrobusRoute = [
      const LatLng(33.4900, 36.2500), // Start (mikrobus stop)
      const LatLng(33.5000, 36.2700),
      const LatLng(33.5100, 36.2900),
      const LatLng(33.5226, 36.3156), // Destination
    ];
    // Simulate user position along the route (static for now)
    final LatLng userPosition = mikrobusRoute[2];

    return Scaffold(
      body: Stack(
        children: [
          FlutterMap(
            options: MapOptions(
              initialCenter: userPosition,
              initialZoom: 13.5,
              interactionOptions: const InteractionOptions(flags: InteractiveFlag.none),
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.example.login_screen',
              ),
              PolylineLayer(
                polylines: [
                  Polyline(
                    points: mikrobusRoute,
                    color: Colors.green,
                    strokeWidth: 6,
                  ),
                ],
              ),
              MarkerLayer(
                markers: [
                  Marker(
                    point: userPosition,
                    width: 40,
                    height: 40,
                    child: Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.teal[700],
                        border: Border.all(color: Colors.white, width: 3),
                      ),
                      child: const Center(
                        child: Icon(Icons.directions_bus, color: Colors.white, size: 24),
                      ),
                    ),
                  ),
                  Marker(
                    point: mikrobusRoute.last,
                    width: 32,
                    height: 32,
                    child: const Icon(Icons.flag, color: Colors.red, size: 28),
                  ),
                ],
              ),
            ],
          ),
          // Top banner for approaching stop
          Positioned(
            top: 40,
            left: 0,
            right: 0,
            child: Center(
              child: ClipRRect(
                borderRadius: const BorderRadius.all(Radius.circular(24)),
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                    decoration: BoxDecoration(
                      color: Colors.amber[700]?.withValues(alpha: 0.92),
                      borderRadius: const BorderRadius.all(Radius.circular(24)),
                      boxShadow: const [
                        BoxShadow(
                          color: Colors.black12,
                          blurRadius: 10,
                          offset: Offset(0, 2),
                        ),
                      ],
                      border: Border.all(color: Colors.white.withValues(alpha: 0.3), width: 1.2),
                    ),
                    child: const Text(
                      'Approaching stop: Al-Mazza – Fayez Mansour Street',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF06332E),
                        fontSize: 15,
                        fontFamily: 'Montserrat',
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
          // End Trip button at bottom
          Positioned(
            bottom: 40,
            left: 32,
            right: 32,
            child: SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                  elevation: 0,
                  backgroundColor: Colors.transparent,
                  shadowColor: Colors.transparent,
                ).copyWith(
                  backgroundColor: WidgetStateProperty.all(Colors.transparent),
                  elevation: WidgetStateProperty.all(0),
                  shadowColor: WidgetStateProperty.all(Colors.transparent),
                  padding: WidgetStateProperty.all(const EdgeInsets.symmetric(vertical: 0, horizontal: 0)),
                  foregroundColor: WidgetStateProperty.all(Colors.transparent),
                  surfaceTintColor: WidgetStateProperty.all(Colors.transparent),
                  overlayColor: WidgetStateProperty.all(Colors.transparent),
                ),
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const TripRatingScreen(),
                    ),
                  );
                },
                child: Ink(
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFF06332E), Color(0xFF0B664E)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Container(
                    alignment: Alignment.center,
                    height: 48,
                    child: const Text(
                      'End Trip',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFF5E9D0),
                        fontFamily: 'Montserrat',
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
} 