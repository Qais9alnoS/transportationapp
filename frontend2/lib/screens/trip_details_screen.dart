import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'trip_tracking_screen.dart';

class TripDetailsScreen extends StatelessWidget {
  final String routeTitle;
  final String routeSummary;
  final List<String> steps;
  const TripDetailsScreen({
    required this.routeTitle,
    required this.routeSummary,
    required this.steps,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Static mock coordinates for demo
    const LatLng start = LatLng(33.4857, 36.2417); // Al-Mazza
    const LatLng mikrobusStop = LatLng(33.4900, 36.2500);
    const LatLng destination = LatLng(33.5226, 36.3156); // Abbasiyyin Square

    return Scaffold(
      appBar: AppBar(
        title: const Text('Trip Details'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        flexibleSpace: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF06332E), Color(0xFF0B664E)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(28),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 12, sigmaY: 12),
                child: Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.22),
                    borderRadius: BorderRadius.circular(28),
                    border: Border.all(color: Colors.white.withValues(alpha: 0.3), width: 1.2),
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 10,
                        offset: Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(routeTitle, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, fontFamily: 'Montserrat', color: Color(0xFF06332E))),
                      const SizedBox(height: 6),
                      Text(routeSummary, style: const TextStyle(fontSize: 14, fontFamily: 'Montserrat', color: Color(0xFF8F8262))),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            ClipRRect(
              borderRadius: BorderRadius.circular(22),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.22),
                    borderRadius: BorderRadius.circular(22),
                    border: Border.all(color: Colors.white.withValues(alpha: 0.3), width: 1.2),
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 8,
                        offset: Offset(0, 2),
                      ),
                    ],
                  ),
                  child: SizedBox(
                    height: 180,
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(16),
                      child: FlutterMap(
                        options: const MapOptions(
                          initialCenter: start,
                          initialZoom: 13.0,
                          interactionOptions: InteractionOptions(flags: InteractiveFlag.none),
                        ),
                        children: [
                          TileLayer(
                            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                            userAgentPackageName: 'com.example.login_screen',
                          ),
                          // Walking segment (blue)
                          PolylineLayer(
                            polylines: [
                              Polyline(
                                points: [start, mikrobusStop],
                                color: Colors.blue,
                                strokeWidth: 5,
                              ),
                            ],
                          ),
                          // Mikrobus segment (green)
                          PolylineLayer(
                            polylines: [
                              Polyline(
                                points: [mikrobusStop, destination],
                                color: Colors.green,
                                strokeWidth: 5,
                              ),
                            ],
                          ),
                          const MarkerLayer(
                            markers: [
                              Marker(
                                point: start,
                                width: 30,
                                height: 30,
                                child: Icon(Icons.directions_walk, color: Colors.blue, size: 28),
                              ),
                              Marker(
                                point: mikrobusStop,
                                width: 30,
                                height: 30,
                                child: Icon(Icons.directions_bus, color: Colors.green, size: 28),
                              ),
                              Marker(
                                point: destination,
                                width: 30,
                                height: 30,
                                child: Icon(Icons.flag, color: Colors.red, size: 28),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            ClipRRect(
              borderRadius: BorderRadius.circular(22),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.22),
                    borderRadius: BorderRadius.circular(22),
                    border: Border.all(color: Colors.white.withValues(alpha: 0.3), width: 1.2),
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 6,
                        offset: Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Instructions:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, fontFamily: 'Montserrat', color: Color(0xFF06332E))),
                      const SizedBox(height: 8),
                      ...steps.asMap().entries.map((entry) => Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('${entry.key + 1}. ', style: const TextStyle(fontWeight: FontWeight.bold, fontFamily: 'Montserrat', color: Color(0xFF8F8262))),
                            Expanded(child: Text(entry.value, style: const TextStyle(fontFamily: 'Montserrat', color: Color(0xFF06332E)))),
                          ],
                        ),
                      )),
                    ],
                  ),
                ),
              ),
            ),
            const Spacer(),
            SizedBox(
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
                      builder: (context) => const TripTrackingScreen(),
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
                      'Start Trip',
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
          ],
        ),
      ),
    );
  }
} 