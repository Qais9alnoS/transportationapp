import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';
import 'dart:ui';

class Destination {
  final String name;
  final LatLng location;
  const Destination(this.name, this.location);
}

class SearchDestinationScreen extends StatefulWidget {
  const SearchDestinationScreen({Key? key}) : super(key: key);

  @override
  State<SearchDestinationScreen> createState() => _SearchDestinationScreenState();
}

class _SearchDestinationScreenState extends State<SearchDestinationScreen> {
  final TextEditingController _controller = TextEditingController();
  String _query = '';

  // Example data
  final List<Destination> _recent = [
    Destination('Home', LatLng(34.7308, 36.7090)),
    Destination('Work', LatLng(34.8021, 38.9968)),
  ];
  final List<Destination> _popular = [
    Destination('Souq Al-Hamidiyah', LatLng(33.5112, 36.3064)),
    Destination('Umayyad Mosque', LatLng(33.5113, 36.3065)),
    Destination('Abbasiyyin Square', LatLng(33.5226, 36.3156)),
    Destination('Al-Mazza', LatLng(33.4857, 36.2417)),
  ];

  List<Destination> get _suggestions {
    if (_query.isEmpty) return [..._recent, ..._popular];
    final all = {..._recent, ..._popular}.toList();
    return all
        .where((d) => d.name.toLowerCase().contains(_query.toLowerCase()))
        .toList();
  }

  void _selectDestination(Destination dest) {
    Navigator.of(context).pop(dest);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Search Destination'),
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
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(28),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 12, sigmaY: 12),
                child: Container(
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
                  child: TextField(
                    controller: _controller,
                    autofocus: true,
                    style: const TextStyle(
                      fontFamily: 'Montserrat',
                      fontWeight: FontWeight.w500,
                      color: Color(0xFF06332E),
                    ),
                    decoration: const InputDecoration(
                      hintText: 'Search for a place...',
                      hintStyle: TextStyle(
                        color: Color(0xFF8F8262),
                        fontFamily: 'Montserrat',
                        fontWeight: FontWeight.w400,
                      ),
                      border: InputBorder.none,
                      prefixIcon: Icon(Icons.search, color: Color(0xFF8F8262)),
                      contentPadding: EdgeInsets.symmetric(vertical: 16, horizontal: 18),
                    ),
                    onChanged: (val) {
                      setState(() {
                        _query = val;
                      });
                    },
                  ),
                ),
              ),
            ),
          ),
          if (_query.isEmpty) ...[
            const _SectionTitle('Recent Destinations'),
            _GlassDestinationList(
              destinations: _recent,
              onTap: _selectDestination,
            ),
            const _SectionTitle('Popular Locations'),
            _GlassDestinationList(
              destinations: _popular,
              onTap: _selectDestination,
            ),
          ] else ...[
            const _SectionTitle('Suggestions'),
            _GlassDestinationList(
              destinations: _suggestions,
              onTap: _selectDestination,
            ),
          ],
        ],
      ),
    );
  }
}

class _GlassDestinationList extends StatelessWidget {
  final List<Destination> destinations;
  final void Function(Destination) onTap;
  const _GlassDestinationList({required this.destinations, required this.onTap, Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: destinations.length,
      separatorBuilder: (_, __) => const SizedBox(height: 10),
      itemBuilder: (context, i) {
        final d = destinations[i];
        return GestureDetector(
          onTap: () => onTap(d),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(22),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
              child: Container(
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
                child: ListTile(
                  leading: const Icon(Icons.place, color: Color(0xFF8F8262)),
                  title: Text(d.name, style: const TextStyle(fontFamily: 'Montserrat', fontWeight: FontWeight.w500, color: Color(0xFF06332E))),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}

class _SectionTitle extends StatelessWidget {
  final String title;
  const _SectionTitle(this.title, {Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, fontFamily: 'Montserrat', color: Color(0xFF06332E))),
    );
  }
} 