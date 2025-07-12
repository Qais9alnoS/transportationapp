import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({Key? key}) : super(key: key);

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  // Map controller to interact with the map programmatically if needed
  final mapController = MapController();

  // Syria coordinates (approximate center)
  final LatLng syriaCenter = const LatLng(34.8, 39.0);
  final double initialZoom = 6.5;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Syria Map'),
        backgroundColor: Theme.of(context).primaryColor,
      ),
      body: Stack(
        children: [
          FlutterMap(
            mapController: mapController,
            options: MapOptions(
              initialCenter: syriaCenter,
              initialZoom: initialZoom,
              minZoom: 3,
              maxZoom: 18,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.example.login_screen',
                // flutter_map automatically caches tiles
                subdomains: const ['a', 'b', 'c'],
              ),
            ],
          ),
          // Add attribution (required by OpenStreetMap usage policy)
          Positioned(
            bottom: 5,
            right: 5,
            child: Container(
              padding: const EdgeInsets.all(3),
              color: Colors.white.withOpacity(0.7),
              child: const Text(
                '© OpenStreetMap contributors',
                style: TextStyle(fontSize: 10, color: Colors.black54),
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Reset map view to initial position
          mapController.move(syriaCenter, initialZoom);
        },
        child: const Icon(Icons.my_location),
      ),
    );
  }
}
