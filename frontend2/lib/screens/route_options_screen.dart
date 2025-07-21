import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';
import 'search_destination_screen.dart';
import 'trip_details_screen.dart';
import 'dart:ui';

class RouteOptionsScreen extends StatefulWidget {
  final LatLng start;
  final Destination destination;
  final String? initialFilter; // 'fastest', 'fewest', 'cheapest', 'nearest'
  final bool offlineMode;
  const RouteOptionsScreen({
    required this.start,
    required this.destination,
    this.initialFilter,
    this.offlineMode = false,
    Key? key,
  }) : super(key: key);

  @override
  State<RouteOptionsScreen> createState() => _RouteOptionsScreenState();
}

class _RouteOptionsScreenState extends State<RouteOptionsScreen> {
  String _selectedFilter = 'fastest';

  @override
  void initState() {
    super.initState();
    if (widget.initialFilter != null) {
      _selectedFilter = widget.initialFilter!;
    }
  }

  void _onSelectFilter(String filter) {
    setState(() {
      _selectedFilter = filter;
    });
  }

  void _onTapRouteCard(int index) {
    // Static mock data for each route
    final routeTitles = [
      'Route 1: Fast path via Al-Mazza',
      'Route 2: Fewer transfers',
      'Route 3: Cheapest',
    ];
    final routeSummaries = [
      'Mikroji Line 1: Al-Mazza → ${widget.destination.name}\nTransfers: 1 mikrobus\nWalk: 5 min\nETA: 20 min\nCost: 500 SYP',
      'Line 2: ${widget.destination.name} via City Center\nTransfers: 0\nWalk: 8 min\nETA: 25 min\nCost: 600 SYP',
      'Line 3: ${widget.destination.name} via Old Town\nTransfers: 2\nWalk: 6 min\nETA: 30 min\nCost: 400 SYP',
    ];
    final stepsList = [
      [
        'Walk 200m northeast to Al-Mazza mikrobus stop (Fayez Mansour Street)',
        'Board mikrobus: Al-Mazza – ${widget.destination.name}',
        'Get off at ${widget.destination.name} station',
      ],
      [
        'Walk 400m to City Center stop',
        'Board mikrobus: City Center – ${widget.destination.name}',
        'Arrive at ${widget.destination.name}',
      ],
      [
        'Walk 150m to Old Town stop',
        'Board mikrobus: Old Town – City Center',
        'Transfer at City Center to mikrobus: City Center – ${widget.destination.name}',
        'Arrive at ${widget.destination.name}',
      ],
    ];
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => TripDetailsScreen(
          routeTitle: routeTitles[index],
          routeSummary: routeSummaries[index],
          steps: stepsList[index],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final bool offlineMode = widget.offlineMode;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Route Options'),
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
            Row(
              children: [
                const Icon(Icons.my_location, color: Colors.blue),
                const SizedBox(width: 8),
                const Text('Start: ', style: TextStyle(fontWeight: FontWeight.bold)),
                Expanded(child: Text('(${widget.start.latitude.toStringAsFixed(4)}, ${widget.start.longitude.toStringAsFixed(4)})')),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Icon(Icons.place, color: Colors.red),
                const SizedBox(width: 8),
                const Text('Destination: ', style: TextStyle(fontWeight: FontWeight.bold)),
                Expanded(child: Text(widget.destination.name)),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _GlassFilterButton(
                  icon: Icons.rocket_launch,
                  label: 'Fastest',
                  selected: _selectedFilter == 'fastest',
                  onTap: () => _onSelectFilter('fastest'),
                ),
                _GlassFilterButton(
                  icon: Icons.compare_arrows,
                  label: 'Fewest Transfers',
                  selected: _selectedFilter == 'fewest',
                  onTap: () => _onSelectFilter('fewest'),
                ),
                _GlassFilterButton(
                  icon: Icons.attach_money,
                  label: 'Cheapest',
                  selected: _selectedFilter == 'cheapest',
                  onTap: () => _onSelectFilter('cheapest'),
                ),
                _GlassFilterButton(
                  icon: Icons.directions_bus,
                  label: 'Nearest Mikrobus',
                  selected: _selectedFilter == 'nearest',
                  onTap: () => _onSelectFilter('nearest'),
                  disabled: offlineMode,
                ),
              ],
            ),
            if (offlineMode)
              Padding(
                padding: const EdgeInsets.only(top: 8.0, left: 8, right: 8),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: const [
                    Icon(Icons.info_outline, color: Colors.grey, size: 18),
                    SizedBox(width: 6),
                    Text('Requires internet connection', style: TextStyle(color: Colors.grey, fontSize: 13, fontFamily: 'Montserrat')),
                  ],
                ),
              ),
            const SizedBox(height: 24),
            Expanded(
              child: ListView(
                children: [
                  _GlassRouteCard(
                    title: 'Route 1: Fast path via Al-Mazza',
                    route: 'Mikroji Line 1: Al-Mazza → ${widget.destination.name}',
                    transfers: 1,
                    walkingTime: 5,
                    arrivalTime: 20,
                    cost: 500,
                    onTap: () => _onTapRouteCard(0),
                  ),
                  const SizedBox(height: 16),
                  _GlassRouteCard(
                    title: 'Route 2: Fewer transfers',
                    route: 'Line 2: ${widget.destination.name} via City Center',
                    transfers: 0,
                    walkingTime: 8,
                    arrivalTime: 25,
                    cost: 600,
                    onTap: () => _onTapRouteCard(1),
                  ),
                  const SizedBox(height: 16),
                  _GlassRouteCard(
                    title: 'Route 3: Cheapest',
                    route: 'Line 3: ${widget.destination.name} via Old Town',
                    transfers: 2,
                    walkingTime: 6,
                    arrivalTime: 30,
                    cost: 400,
                    onTap: () => _onTapRouteCard(2),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _GlassFilterButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onTap;
  final bool disabled;
  const _GlassFilterButton({
    required this.icon,
    required this.label,
    required this.selected,
    required this.onTap,
    this.disabled = false,
    Key? key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: disabled ? null : onTap,
      child: Opacity(
        opacity: disabled ? 0.4 : 1.0,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(22),
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                gradient: selected
                    ? const LinearGradient(
                        colors: [Color(0xFF06332E), Color(0xFF0B664E)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      )
                    : null,
                color: selected ? null : Colors.white.withOpacity(0.22),
                borderRadius: BorderRadius.circular(22),
                border: Border.all(color: Colors.white.withOpacity(0.3), width: 1.2),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 8,
                    offset: Offset(0, 2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Icon(icon, color: selected ? Color(0xFFF5E9D0) : Color(0xFF06332E), size: 18),
                  const SizedBox(width: 6),
                  Text(
                    label,
                    style: TextStyle(
                      color: selected ? Color(0xFFF5E9D0) : Color(0xFF06332E),
                      fontWeight: FontWeight.bold,
                      fontSize: 13,
                      fontFamily: 'Montserrat',
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _GlassRouteCard extends StatelessWidget {
  final String title;
  final String route;
  final int transfers;
  final int walkingTime;
  final int arrivalTime;
  final int cost;
  final VoidCallback onTap;
  const _GlassRouteCard({
    required this.title,
    required this.route,
    required this.transfers,
    required this.walkingTime,
    required this.arrivalTime,
    required this.cost,
    required this.onTap,
    Key? key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(28),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.22),
              borderRadius: BorderRadius.circular(28),
              border: Border.all(color: Colors.white.withOpacity(0.3), width: 1.2),
              boxShadow: [
                BoxShadow(
                  color: Colors.black12,
                  blurRadius: 12,
                  offset: Offset(0, 4),
                ),
              ],
            ),
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 17, fontFamily: 'Montserrat', color: Color(0xFF06332E))),
                const SizedBox(height: 6),
                Text(route, style: const TextStyle(fontSize: 14, fontFamily: 'Montserrat', color: Color(0xFF8F8262))),
                const SizedBox(height: 14),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    _GlassRouteInfo(icon: Icons.transfer_within_a_station, label: 'Transfers', value: '$transfers'),
                    _GlassRouteInfo(icon: Icons.directions_walk, label: 'Walk', value: '$walkingTime min'),
                    _GlassRouteInfo(icon: Icons.access_time, label: 'ETA', value: '$arrivalTime min'),
                    _GlassRouteInfo(icon: Icons.attach_money, label: '', value: '$cost SYP'),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _GlassRouteInfo extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  const _GlassRouteInfo({required this.icon, required this.label, required this.value, Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 16, color: Color(0xFF8F8262)),
        const SizedBox(width: 3),
        if (label.isNotEmpty)
          Text('$label: ', style: const TextStyle(fontSize: 13, color: Color(0xFF8F8262), fontFamily: 'Montserrat', fontWeight: FontWeight.w500)),
        Text(value, style: const TextStyle(fontSize: 13, color: Color(0xFF06332E), fontFamily: 'Montserrat', fontWeight: FontWeight.bold)),
      ],
    );
  }
} 