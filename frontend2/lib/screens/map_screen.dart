import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:location/location.dart' as location_package;
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import 'friends_page.dart';
import 'login_screen/login_screen.dart';
import 'dart:ui';
import 'dart:math';

class MapScreen extends StatefulWidget {
  const MapScreen({Key? key}) : super(key: key);

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> with TickerProviderStateMixin {
  final mapController = MapController();
  final LatLng damascusCenter = const LatLng(33.5138, 36.2765);
  final double damascusZoom = 13.0;

  location_package.LocationData? _currentLocation;
  bool _serviceEnabled = false;
  location_package.PermissionStatus? _permissionGranted;
  final location_package.Location _location = location_package.Location();

  LatLng? _selectedPin;
  LatLng? _startingPoint;
  String? _selectedRouteOption;
  RouteData? _selectedRoute; // Only one route now
  final bool offlineMode = false;

  // Friend location tracking
  Friend? _locatedFriend;

  // Animation controllers
  late AnimationController _searchAnimationController;
  late AnimationController _generalAnimationController;
  late AnimationController _sideMenuController;
  late AnimationController _bottomPanelController;
  late AnimationController _routeTransitionController;
  late AnimationController _favoriteDialogController;
  late AnimationController _notificationController;
  late AnimationController
      _locationMoveController; // New for smooth location transition

  // Animations
  late Animation<double> _searchWidthAnimation;
  late Animation<double> _searchHeightAnimation;
  late Animation<double> _searchOpacityAnimation;
  late Animation<double> _buttonScaleAnimation;
  late Animation<double> _buttonOpacityAnimation;
  late Animation<Offset> _sideMenuAnimation;
  late Animation<Offset> _bottomPanelAnimation;
  late Animation<double> _routeTransitionAnimation;
  late Animation<double> _favoriteDialogScale;
  late Animation<double> _favoriteDialogOpacity;
  late Animation<Offset> _notificationSlideAnimation;
  late Animation<double> _notificationOpacityAnimation;

  bool _isSearchExpanded = false;
  bool _isSideMenuOpen = false;
  bool _isBottomPanelOpen = false;
  bool _isTransitioningToRoutes = false;
  bool _showFavoriteDialog = false;
  bool _isSelectingStartingPoint = false;
  bool _showNotification = false;
  String _notificationText = '';
  IconData _notificationIcon = Icons.info;
  Color _notificationColor = Color(0xFF06332E);
  String _startingButtonText = "Starting Location";

  final TextEditingController _searchController = TextEditingController();
  final TextEditingController _favoriteNameController = TextEditingController();
  final FocusNode _searchFocusNode = FocusNode();
  final FocusNode _favoriteNameFocusNode = FocusNode();

  final GlobalKey<_PinWithAnimatedButtonsState> _pinAnimKey = GlobalKey();

  final List<SearchLocationData> _allLocations = [
    SearchLocationData('Home', LatLng(33.5138, 36.2765)),
    SearchLocationData('Work', LatLng(33.5200, 36.2800)),
    SearchLocationData('School', LatLng(33.5100, 36.2700)),
    SearchLocationData('Hospital', LatLng(33.5180, 36.2750)),
    SearchLocationData('Mall', LatLng(33.5120, 36.2780)),
    SearchLocationData('Airport', LatLng(33.4100, 36.5150)),
    SearchLocationData('University', LatLng(33.5250, 36.2850)),
    SearchLocationData('Park', LatLng(33.5080, 36.2720)),
    SearchLocationData('Restaurant', LatLng(33.5160, 36.2790)),
    SearchLocationData('Hotel', LatLng(33.5190, 36.2810)),
  ];

  List<SearchLocationData> get _filteredLocations {
    if (_searchController.text.isEmpty) {
      return _allLocations.take(3).toList();
    }
    return _allLocations
        .where((location) => location.name
            .toLowerCase()
            .contains(_searchController.text.toLowerCase()))
        .take(3)
        .toList();
  }

  void _onMapTap(TapPosition tapPosition, LatLng latlng) {
    if (_isSelectingStartingPoint) {
      _setStartingPoint(latlng);
      return;
    }

    if (_isSearchExpanded) {
      _collapseSearch();
    }

    if (_isSideMenuOpen) {
      _closeSideMenu();
    }

    if (_isBottomPanelOpen) {
      _closeBottomPanel();
    }

    if (_showFavoriteDialog) {
      _closeFavoriteDialog();
    }

    _pinAnimKey.currentState?.resetAnimation();

    setState(() {
      _selectedPin = latlng;
      _selectedRouteOption = null;
      _selectedRoute = null;
      _isTransitioningToRoutes = false;
    });

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _pinAnimKey.currentState?.playForward();
    });
  }

  void _onMapMove(MapPosition pos, bool hasGesture) {
    if (_selectedRouteOption != null) return;

    if (_selectedPin != null && hasGesture) {
      _pinAnimKey.currentState?.playReverse(onComplete: () {
        setState(() {
          _selectedPin = null;
          _selectedRouteOption = null;
          _selectedRoute = null;
          _isTransitioningToRoutes = false;
        });
      });
    }
  }

  void _onSelectRouteOption(String option) {
    if (_startingPoint == null && _currentLocation == null) {
      _showStartingPointError();
      return;
    }

    setState(() {
      _selectedRouteOption = option;
      _isTransitioningToRoutes = true;
    });

    _routeTransitionController.forward().then((_) {
      setState(() {
        _selectedRoute =
            _generateSingleRoute(option); // Generate only one route
      });

      // Automatically open bottom panel with route details
      _openBottomPanel();
    });
  }

  void _showStartingPointError() {
    _showCustomNotification(
      'Please set a starting point first using the Starting Location button',
      Icons.error_outline,
      Colors.red.shade600,
    );
  }

  void _onGo() async {
    if (_selectedRoute == null) return;

    // Smoothly slide down the panel
    _bottomPanelController
        .animateTo(0.0,
            duration: Duration(milliseconds: 500), curve: Curves.easeInOutCubic)
        .then((_) {
      setState(() {
        _isBottomPanelOpen = false;
        _selectedPin = null;
        _selectedRouteOption = null;
        _selectedRoute = null;
        _isTransitioningToRoutes = false;
      });
    });

    print('Going with route: ${_selectedRoute!.name}');
  }

  void _onSetStartingPoint() {
    if (!_isSelectingStartingPoint) {
      setState(() {
        _isSelectingStartingPoint = true;
        _startingButtonText = "Select";
      });
    } else {
      _cancelStartingPointSelection();
    }
  }

  void _setStartingPoint(LatLng latlng) {
    setState(() {
      _startingPoint = latlng;
      _isSelectingStartingPoint = false;
      _startingButtonText = "Cancel";
    });
  }

  void _cancelStartingPointSelection() {
    setState(() {
      _startingPoint = null;
      _isSelectingStartingPoint = false;
      _startingButtonText = "Starting Location";
    });
  }

  void _onMakeFavorite() {
    if (_selectedPin != null) {
      setState(() {
        _showFavoriteDialog = true;
      });
      _favoriteDialogController.forward();
      Future.delayed(Duration(milliseconds: 300), () {
        _favoriteNameFocusNode.requestFocus();
      });
    }
  }

  void _closeFavoriteDialog() {
    _favoriteNameFocusNode.unfocus();
    _favoriteDialogController.reverse().then((_) {
      setState(() {
        _showFavoriteDialog = false;
        _favoriteNameController.clear();
      });
    });
  }

  void _addFavoriteLocation() {
    final name = _favoriteNameController.text.trim();
    if (name.isNotEmpty) {
      print('Adding favorite: $name at ${_selectedPin.toString()}');

      _showCustomNotification(
        'Location "$name" added to favorites!',
        Icons.favorite,
        Color(0xFF06332E),
      );

      _closeFavoriteDialog();
    }
  }

  // Generate only one route instead of multiple
  RouteData _generateSingleRoute(String type) {
    final random = Random();
    return RouteData(
      name: '$type Route',
      duration: '${15 + random.nextInt(20)} min',
      distance: '${2 + random.nextInt(8)}.${random.nextInt(10)} km',
      cost: '\$${3 + random.nextInt(7)}',
      points: _generateRoutePoints(0),
      color: Color(0xFF06332E),
    );
  }

  List<LatLng> _generateRoutePoints(int routeIndex) {
    final start = _startingPoint ??
        (_currentLocation != null
            ? LatLng(_currentLocation!.latitude!, _currentLocation!.longitude!)
            : damascusCenter);
    final end = _selectedPin!;

    List<LatLng> points = [start];

    final latDiff = (end.latitude - start.latitude) / 4;
    final lngDiff = (end.longitude - start.longitude) / 4;
    final random = Random(routeIndex);

    for (int i = 1; i < 4; i++) {
      points.add(LatLng(
        start.latitude + (latDiff * i) + (random.nextDouble() - 0.5) * 0.01,
        start.longitude + (lngDiff * i) + (random.nextDouble() - 0.5) * 0.01,
      ));
    }

    points.add(end);
    return points;
  }

  void _expandSearch() {
    setState(() {
      _isSearchExpanded = true;
    });
    _searchAnimationController.forward();
    Future.delayed(const Duration(milliseconds: 400), () {
      _searchFocusNode.requestFocus();
    });
  }

  void _collapseSearch() {
    _searchFocusNode.unfocus();
    // Faster fade away animation - reduced duration
    _searchAnimationController.reverse(from: 1.0).then((_) {
      setState(() {
        _isSearchExpanded = false;
      });
    });
  }

  void _openSideMenu() {
    setState(() {
      _isSideMenuOpen = true;
    });
    _sideMenuController.forward();
  }

  void _closeSideMenu() {
    _sideMenuController.reverse().then((_) {
      setState(() {
        _isSideMenuOpen = false;
      });
    });
  }

  void _openBottomPanel() {
    setState(() {
      _isBottomPanelOpen = true;
    });
    _bottomPanelController.forward();
  }

  void _closeBottomPanel() {
    _bottomPanelController.reverse().then((_) {
      setState(() {
        _isBottomPanelOpen = false;
      });
    });
  }

  // Smooth location transition
  void _moveToUserLocation() {
    final LatLng? userLatLng = _currentLocation != null
        ? LatLng(_currentLocation!.latitude!, _currentLocation!.longitude!)
        : null;

    if (userLatLng != null) {
      // Get current map center and zoom
      final currentCenter = mapController.center;
      final currentZoom = mapController.zoom;
      final targetZoom = 15.0;

      // Animation duration
      const animationDuration = Duration(milliseconds: 800);

      // Create animation controllers for smooth transition
      AnimationController latController = AnimationController(
        duration: animationDuration,
        vsync: this,
      );

      AnimationController lngController = AnimationController(
        duration: animationDuration,
        vsync: this,
      );

      AnimationController zoomController = AnimationController(
        duration: animationDuration,
        vsync: this,
      );

      // Create animations
      Animation<double> latAnimation = Tween<double>(
        begin: currentCenter.latitude,
        end: userLatLng.latitude,
      ).animate(CurvedAnimation(
        parent: latController,
        curve: Curves.easeInOut,
      ));

      Animation<double> lngAnimation = Tween<double>(
        begin: currentCenter.longitude,
        end: userLatLng.longitude,
      ).animate(CurvedAnimation(
        parent: lngController,
        curve: Curves.easeInOut,
      ));

      Animation<double> zoomAnimation = Tween<double>(
        begin: currentZoom,
        end: targetZoom,
      ).animate(CurvedAnimation(
        parent: zoomController,
        curve: Curves.easeInOut,
      ));

      // Add listeners to update map position
      void updateMap() {
        mapController.move(
          LatLng(latAnimation.value, lngAnimation.value),
          zoomAnimation.value,
        );
      }

      latController.addListener(updateMap);
      lngController.addListener(updateMap);
      zoomController.addListener(updateMap);

      // Start animations
      latController.forward();
      lngController.forward();
      zoomController.forward();

      // Dispose controllers after animation completes
      Future.delayed(animationDuration, () {
        latController.dispose();
        lngController.dispose();
        zoomController.dispose();
      });
    }
  }

  void _onSearchSubmitted(String query) async {
    if (query.trim().isEmpty) return;

    final matchingLocation = _allLocations.firstWhere(
      (location) => location.name.toLowerCase() == query.toLowerCase(),
      orElse: () => _allLocations.first,
    );

    _collapseSearch();
    _placePin(matchingLocation.location);
    _searchController.clear();
  }

  void _onSuggestionTapped(SearchLocationData location) {
    _collapseSearch();
    _placePin(location.location);
    _searchController.clear();
  }

  void _placePin(LatLng location) {
    _pinAnimKey.currentState?.resetAnimation();

    setState(() {
      _selectedPin = location;
      _selectedRouteOption = null;
      _selectedRoute = null;
      _isTransitioningToRoutes = false;
    });

    mapController.move(location, damascusZoom);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _pinAnimKey.currentState?.playForward();
    });
  }

  void _showCustomNotification(String text, IconData icon, Color color) {
    setState(() {
      _notificationText = text;
      _notificationIcon = icon;
      _notificationColor = color;
      _showNotification = true;
    });

    _notificationController.forward().then((_) {
      Future.delayed(Duration(seconds: 6), () {
        _hideCustomNotification();
      });
    });
  }

  void _hideCustomNotification() {
    _notificationController.reverse().then((_) {
      setState(() {
        _showNotification = false;
      });
    });
  }

  // Navigation functions
  void _navigateToFriends() async {
    _closeSideMenu();
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => FriendsPage()),
    );

    // Check if a friend was returned (located)
    if (result != null && result is Friend) {
      // Add friend marker to the map
      setState(() {
        // Store the friend for marker display
        _locatedFriend = result;
      });

      // Move map to friend's location
      mapController.move(result.location, 15.0);
    }
  }

  void _signOut() async {
    // Close the side menu first
    _closeSideMenu();

    // Use AuthProvider to sign out
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    await authProvider.logout();

    // Navigate to login screen and remove all previous routes
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (context) => const LoginScreen()),
      (route) => false,
    );
  }

  @override
  void initState() {
    super.initState();
    _initLocation();
    _initAnimationControllers();
    _searchController.addListener(() {
      setState(() {});
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _initAnimations();
  }

  void _initAnimationControllers() {
    _searchAnimationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400), // Faster fade away
    );

    _generalAnimationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );

    _sideMenuController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );

    _bottomPanelController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );

    _routeTransitionController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );

    _favoriteDialogController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400),
    );

    _notificationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );

    _locationMoveController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
  }

  void _initAnimations() {
    final screenWidth = MediaQuery.of(context).size.width;

    _searchWidthAnimation = Tween<double>(
      begin: 300.0,
      end: screenWidth - 80,
    ).animate(CurvedAnimation(
      parent: _searchAnimationController,
      curve: Curves.easeOutBack,
    ));

    _searchHeightAnimation = Tween<double>(
      begin: 60.0,
      end: 350.0,
    ).animate(CurvedAnimation(
      parent: _searchAnimationController,
      curve: Curves.elasticOut,
    ));

    _searchOpacityAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _searchAnimationController,
      curve: const Interval(0.3, 1.0, curve: Curves.easeOutCubic),
    ));

    _buttonScaleAnimation = Tween<double>(
      begin: 0.8,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _generalAnimationController,
      curve: Curves.elasticOut,
    ));

    _buttonOpacityAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _generalAnimationController,
      curve: const Interval(0.2, 1.0, curve: Curves.easeIn),
    ));

    _sideMenuAnimation = Tween<Offset>(
      begin: const Offset(1.0, 0.0),
      end: const Offset(0.0, 0.0),
    ).animate(CurvedAnimation(
      parent: _sideMenuController,
      curve: Curves.easeOutCubic,
    ));

    _bottomPanelAnimation = Tween<Offset>(
      begin: const Offset(0.0, 1.0),
      end: const Offset(0.0, 0.0),
    ).animate(CurvedAnimation(
      parent: _bottomPanelController,
      curve: Curves.easeOutCubic,
    ));

    _routeTransitionAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _routeTransitionController,
      curve: Curves.easeInOutCubic,
    ));

    _favoriteDialogScale = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _favoriteDialogController,
      curve: Curves.elasticOut,
    ));

    _favoriteDialogOpacity = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _favoriteDialogController,
      curve: Curves.easeOut,
    ));

    _notificationSlideAnimation = Tween<Offset>(
      begin: const Offset(0.0, -1.0),
      end: const Offset(0.0, 0.0),
    ).animate(CurvedAnimation(
      parent: _notificationController,
      curve: Curves.easeOutBack,
    ));

    _notificationOpacityAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _notificationController,
      curve: Curves.easeOut,
    ));

    _generalAnimationController.forward();
  }

  Future<void> _initLocation() async {
    _serviceEnabled = await _location.serviceEnabled();
    if (!_serviceEnabled) {
      _serviceEnabled = await _location.requestService();
      if (!_serviceEnabled) return;
    }
    _permissionGranted = await _location.hasPermission();
    if (_permissionGranted != location_package.PermissionStatus.granted) {
      _permissionGranted = await _location.requestPermission();
      if (_permissionGranted != location_package.PermissionStatus.granted)
        return;
    }
    final loc = await _location.getLocation();
    setState(() {
      _currentLocation = loc;
    });
    _location.onLocationChanged.listen((loc) {
      setState(() {
        _currentLocation = loc;
      });
    });
  }

  @override
  void dispose() {
    _searchAnimationController.dispose();
    _generalAnimationController.dispose();
    _sideMenuController.dispose();
    _bottomPanelController.dispose();
    _routeTransitionController.dispose();
    _favoriteDialogController.dispose();
    _notificationController.dispose();
    _locationMoveController.dispose();
    _searchController.dispose();
    _favoriteNameController.dispose();
    _searchFocusNode.dispose();
    _favoriteNameFocusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final LatLng? userLatLng = _currentLocation != null
        ? LatLng(_currentLocation!.latitude ?? damascusCenter.latitude,
            _currentLocation!.longitude ?? damascusCenter.longitude)
        : null;
    return Scaffold(
      body: Stack(
        children: [
          FlutterMap(
            mapController: mapController,
            options: MapOptions(
              initialCenter: damascusCenter,
              initialZoom: damascusZoom,
              minZoom: damascusZoom,
              maxZoom: 18,
              onTap: _onMapTap,
              onPositionChanged: _onMapMove,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.example.login_screen',
                subdomains: const ['a', 'b', 'c'],
              ),

              // Single route line
              if (_selectedRoute != null)
                PolylineLayer(
                  polylines: [
                    Polyline(
                      points: _selectedRoute!.points,
                      strokeWidth: 6.0,
                      color: _selectedRoute!.color.withOpacity(0.9),
                    ),
                  ],
                ),

              if (userLatLng != null)
                MarkerLayer(
                  markers: [
                    Marker(
                      point: userLatLng,
                      width: 36,
                      height: 36,
                      child: AnimatedBuilder(
                        animation: _buttonScaleAnimation,
                        builder: (context, child) => Transform.scale(
                          scale: _buttonScaleAnimation.value,
                          child: Container(
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              gradient: LinearGradient(
                                colors: [
                                  Color(0xFF06332E),
                                  Color(0xFF0B664E),
                                ],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              border: Border.all(
                                  color: Color(0xFFF5E9D0), width: 4),
                            ),
                            child: const Center(
                              child: Icon(Icons.my_location,
                                  color: Color(0xFFF5E9D0), size: 20),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),

              if (_startingPoint != null)
                MarkerLayer(
                  markers: [
                    Marker(
                      point: _startingPoint!,
                      width: 48,
                      height: 48,
                      alignment: Alignment(0.0, -0.7),
                      child: Container(
                        child: Stack(
                          alignment: Alignment.center,
                          children: [
                            Positioned(
                              top: 2,
                              child: Container(
                                width: 40,
                                height: 40,
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  color: Colors.black.withOpacity(0.15),
                                ),
                              ),
                            ),
                            ShaderMask(
                              shaderCallback: (bounds) => LinearGradient(
                                colors: [
                                  Color(0xFF06332E),
                                  Color(0xFF0B664E),
                                ],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ).createShader(bounds),
                              child: Icon(
                                Icons.location_on,
                                color: Colors.white,
                                size: 40,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),

              if (_selectedPin != null)
                MarkerLayer(
                  markers: [
                    Marker(
                      point: _selectedPin!,
                      width: 400,
                      height: 280,
                      alignment: Alignment(0.0, 0.35),
                      child: _PinWithAnimatedButtons(
                        key: _pinAnimKey,
                        selected: _selectedRouteOption,
                        onSelect: _onSelectRouteOption,
                        onGo: _onGo,
                        onMakeFavorite: _onMakeFavorite,
                        selectedRoute: _selectedRoute,
                        isTransitioning: _isTransitioningToRoutes,
                        transitionAnimation: _routeTransitionAnimation,
                      ),
                    ),
                  ],
                ),

              // Friend location marker
              if (_locatedFriend != null)
                MarkerLayer(
                  markers: [
                    Marker(
                      point: _locatedFriend!.location,
                      width: 100,
                      height: 100,
                      alignment: Alignment(0.0, 0.0),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 50,
                            height: 50,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: Color(0xFF06332E),
                              border: Border.all(
                                color: Color(0xFFF5E9D0),
                                width: 2,
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.3),
                                  blurRadius: 6,
                                  offset: Offset(0, 3),
                                ),
                              ],
                            ),
                            child: ClipOval(
                              child: Image.network(
                                _locatedFriend!.profilePicture,
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) {
                                  return Container(
                                    color: Color(0xFFF5E9D0).withOpacity(0.3),
                                    child: Icon(
                                      Icons.person,
                                      color: Color(0xFF06332E),
                                      size: 24,
                                    ),
                                  );
                                },
                              ),
                            ),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(
                                horizontal: 8, vertical: 4),
                            margin: EdgeInsets.only(top: 8),
                            constraints: BoxConstraints(
                              minWidth: 40,
                              maxWidth: 120,
                            ),
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [
                                  Color(0xFF06332E),
                                  Color(0xFF0B664E),
                                ],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              borderRadius: BorderRadius.circular(12),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.2),
                                  blurRadius: 4,
                                  offset: Offset(0, 2),
                                ),
                              ],
                              border: Border.all(
                                color: Color(0xFFF5E9D0),
                                width: 1.5,
                              ),
                            ),
                            child: Text(
                              _locatedFriend!.name
                                  .split(' ')[0], // Just the first name
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                color: Color(0xFFF5E9D0),
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
            ],
          ),

          // Enhanced Search bar with faster animation
          Positioned(
            top: 50,
            left: 16,
            child: AnimatedBuilder(
              animation: _searchAnimationController,
              builder: (context, child) {
                return LayoutBuilder(
                  builder: (context, constraints) {
                    final maxWidth = MediaQuery.of(context).size.width - 80;
                    final currentWidth =
                        _isSearchExpanded ? (maxWidth * 0.95) : 300.0;

                    final suggestionsCount = _filteredLocations.length;
                    final targetHeight = _isSearchExpanded
                        ? (90.0 + (suggestionsCount * 70.0) + 50.0)
                            .clamp(90.0, 600.0)
                        : 70.0;

                    return GestureDetector(
                      onTap: _isSearchExpanded ? null : _expandSearch,
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(28),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
                          child: AnimatedContainer(
                            duration:
                                Duration(milliseconds: 200), // Faster animation
                            curve: Curves.easeOutCubic,
                            width: currentWidth,
                            height: targetHeight,
                            clipBehavior: Clip.hardEdge,
                            constraints: BoxConstraints(
                              minHeight: 70.0,
                              maxHeight: 600.0,
                            ),
                            padding: const EdgeInsets.symmetric(
                                horizontal: 24, vertical: 20),
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [
                                  Color(0xFF0B664E).withOpacity(0.9),
                                  Color(0xFF06332E).withOpacity(0.85),
                                ],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              borderRadius: BorderRadius.circular(28),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.15),
                                  blurRadius: 20,
                                  offset: Offset(0, 8),
                                ),
                              ],
                              border: Border.all(
                                  color: Color(0xFF0F7A5A), width: 1.5),
                            ),
                            child: SingleChildScrollView(
                              physics: NeverScrollableScrollPhysics(),
                              child: _isSearchExpanded
                                  ? Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Row(
                                          children: [
                                            Icon(Icons.search,
                                                color: Color(0xFFF5E9D0)),
                                            SizedBox(width: 10),
                                            Expanded(
                                              child: AnimatedOpacity(
                                                opacity: _searchOpacityAnimation
                                                    .value,
                                                duration: Duration(
                                                    milliseconds:
                                                        200), // Faster
                                                child: TextField(
                                                  controller: _searchController,
                                                  focusNode: _searchFocusNode,
                                                  onSubmitted:
                                                      _onSearchSubmitted,
                                                  style: TextStyle(
                                                    fontSize: 16,
                                                    color: Color(0xFFF5E9D0),
                                                    fontFamily: 'Montserrat',
                                                    fontWeight: FontWeight.w500,
                                                  ),
                                                  decoration: InputDecoration(
                                                    hintText:
                                                        'Where do you want to go?',
                                                    hintStyle: TextStyle(
                                                      color: Color(0xFFF5E9D0)
                                                          .withOpacity(0.7),
                                                    ),
                                                    border: InputBorder.none,
                                                    contentPadding:
                                                        EdgeInsets.zero,
                                                  ),
                                                ),
                                              ),
                                            ),
                                            AnimatedOpacity(
                                              opacity:
                                                  _searchOpacityAnimation.value,
                                              duration: Duration(
                                                  milliseconds: 200), // Faster
                                              child: GestureDetector(
                                                onTap: _collapseSearch,
                                                child: Icon(Icons.close,
                                                    color: Color(0xFFF5E9D0)),
                                              ),
                                            ),
                                          ],
                                        ),
                                        if (_isSearchExpanded &&
                                            _filteredLocations.isNotEmpty) ...[
                                          SizedBox(
                                              height: 12), // Reduced spacing
                                          AnimatedOpacity(
                                            opacity:
                                                _searchOpacityAnimation.value,
                                            duration: Duration(
                                                milliseconds: 300), // Faster
                                            child: Column(
                                              crossAxisAlignment:
                                                  CrossAxisAlignment.start,
                                              mainAxisSize: MainAxisSize.min,
                                              children: [
                                                ..._filteredLocations
                                                    .map(
                                                      (location) => Container(
                                                        clipBehavior:
                                                            Clip.hardEdge,
                                                        decoration:
                                                            BoxDecoration(
                                                          borderRadius:
                                                              BorderRadius
                                                                  .circular(16),
                                                        ),
                                                        child: GestureDetector(
                                                          onTap: () =>
                                                              _onSuggestionTapped(
                                                                  location),
                                                          child: Container(
                                                            width:
                                                                double.infinity,
                                                            padding: EdgeInsets
                                                                .symmetric(
                                                                    vertical:
                                                                        16,
                                                                    horizontal:
                                                                        18),
                                                            margin:
                                                                EdgeInsets.only(
                                                                    bottom: 12),
                                                            decoration:
                                                                BoxDecoration(
                                                              gradient:
                                                                  LinearGradient(
                                                                colors: [
                                                                  Color(0xFFF5E9D0)
                                                                      .withOpacity(
                                                                          0.25),
                                                                  Color(0xFFF5E9D0)
                                                                      .withOpacity(
                                                                          0.15),
                                                                ],
                                                              ),
                                                              borderRadius:
                                                                  BorderRadius
                                                                      .circular(
                                                                          16),
                                                              border:
                                                                  Border.all(
                                                                color: Color(
                                                                        0xFFF5E9D0)
                                                                    .withOpacity(
                                                                        0.4),
                                                                width: 1.5,
                                                              ),
                                                            ),
                                                            child: Row(
                                                              children: [
                                                                Icon(
                                                                  _getLocationIcon(
                                                                      location
                                                                          .name),
                                                                  color: Color(
                                                                      0xFFF5E9D0),
                                                                  size: 20,
                                                                ),
                                                                SizedBox(
                                                                    width: 14),
                                                                Expanded(
                                                                  child: Text(
                                                                    location
                                                                        .name,
                                                                    style:
                                                                        TextStyle(
                                                                      fontSize:
                                                                          16,
                                                                      color: Color(
                                                                          0xFFF5E9D0),
                                                                      fontFamily:
                                                                          'Montserrat',
                                                                      fontWeight:
                                                                          FontWeight
                                                                              .w600,
                                                                    ),
                                                                    overflow:
                                                                        TextOverflow
                                                                            .ellipsis,
                                                                  ),
                                                                ),
                                                              ],
                                                            ),
                                                          ),
                                                        ),
                                                      ),
                                                    )
                                                    .toList(),
                                              ],
                                            ),
                                          ),
                                        ],
                                      ],
                                    )
                                  : Row(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Icon(Icons.search,
                                            color: Color(0xFFF5E9D0)),
                                        SizedBox(width: 10),
                                        Text(
                                          'Where do you want to go?',
                                          style: TextStyle(
                                            fontSize: 16,
                                            color: Color(0xFFF5E9D0),
                                            fontFamily: 'Montserrat',
                                            fontWeight: FontWeight.w500,
                                          ),
                                        ),
                                      ],
                                    ),
                            ),
                          ),
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),

          // Enhanced Menu icon
          Positioned(
            top: 50,
            right: 16,
            child: AnimatedBuilder(
              animation: _buttonScaleAnimation,
              builder: (context, child) => Transform.scale(
                scale: _buttonScaleAnimation.value,
                child: AnimatedOpacity(
                  opacity: _buttonOpacityAnimation.value,
                  duration: Duration(milliseconds: 300),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(20),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              Color(0xFF06332E).withOpacity(0.8),
                              Color(0xFF0B664E).withOpacity(0.8),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                          borderRadius: BorderRadius.circular(20),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.2),
                              blurRadius: 15,
                              offset: Offset(0, 5),
                            ),
                          ],
                          border:
                              Border.all(color: Color(0xFF0F7A5A), width: 1.5),
                        ),
                        child: IconButton(
                          icon: Icon(Icons.menu,
                              color: Color(0xFFF5E9D0), size: 32),
                          onPressed: _openSideMenu,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Enhanced Starting Location button
          Positioned(
            bottom: 40,
            right: 16,
            child: AnimatedBuilder(
              animation: _buttonScaleAnimation,
              builder: (context, child) => Transform.scale(
                scale: _buttonScaleAnimation.value,
                child: AnimatedOpacity(
                  opacity: _buttonOpacityAnimation.value,
                  duration: Duration(milliseconds: 400),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(28),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
                      child: GestureDetector(
                        onTap: _onSetStartingPoint,
                        child: AnimatedContainer(
                          duration: Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                          padding: EdgeInsets.symmetric(
                              horizontal: 20, vertical: 12),
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Color(0xFF06332E).withOpacity(0.85),
                                Color(0xFF0B664E).withOpacity(0.85),
                              ],
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                            ),
                            borderRadius: BorderRadius.circular(28),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.2),
                                blurRadius: 15,
                                offset: Offset(0, 5),
                              ),
                            ],
                            border: Border.all(
                                color: Color(0xFF0F7A5A), width: 1.5),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.add_location_alt,
                                  color: Color(0xFFF5E9D0), size: 24),
                              SizedBox(width: 8),
                              AnimatedSwitcher(
                                duration: Duration(milliseconds: 300),
                                child: Text(
                                  _startingButtonText,
                                  key: ValueKey(_startingButtonText),
                                  style: TextStyle(
                                    color: Color(0xFFF5E9D0),
                                    fontSize: 14,
                                    fontWeight: FontWeight.w600,
                                    fontFamily: 'Montserrat',
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Enhanced Recenter button with smooth transition
          Positioned(
            bottom: 40,
            left: 16,
            child: AnimatedBuilder(
              animation: _buttonScaleAnimation,
              builder: (context, child) => Transform.scale(
                scale: _buttonScaleAnimation.value,
                child: AnimatedOpacity(
                  opacity: _buttonOpacityAnimation.value,
                  duration: Duration(milliseconds: 500),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(24),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              Color(0xFF06332E).withOpacity(0.8),
                              Color(0xFF0B664E).withOpacity(0.8),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                          borderRadius: BorderRadius.circular(24),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.2),
                              blurRadius: 15,
                              offset: Offset(0, 5),
                            ),
                          ],
                          border:
                              Border.all(color: Color(0xFF0F7A5A), width: 1.5),
                        ),
                        child: FloatingActionButton(
                          heroTag: 'recenter',
                          backgroundColor: Colors.transparent,
                          elevation: 0,
                          onPressed:
                              _moveToUserLocation, // Use smooth transition
                          child: Icon(Icons.my_location,
                              color: Color(0xFFF5E9D0), size: 28),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Enhanced Side Menu Panel
          if (_isSideMenuOpen)
            GestureDetector(
              onTap: _closeSideMenu,
              child: Container(
                color: Colors.black.withOpacity(0.3),
                child: Stack(
                  children: [
                    SlideTransition(
                      position: _sideMenuAnimation,
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: Container(
                          width: 320, // Wider menu
                          height: double.infinity,
                          child: ClipRRect(
                            borderRadius: BorderRadius.only(
                              topLeft: Radius.circular(24),
                              bottomLeft: Radius.circular(24),
                            ),
                            child: BackdropFilter(
                              filter: ImageFilter.blur(sigmaX: 25, sigmaY: 25),
                              child: Container(
                                decoration: BoxDecoration(
                                  gradient: LinearGradient(
                                    colors: [
                                      Color(0xFF06332E).withOpacity(0.95),
                                      Color(0xFF0B664E).withOpacity(0.95),
                                    ],
                                    begin: Alignment.topLeft,
                                    end: Alignment.bottomRight,
                                  ),
                                  border: Border.all(
                                    color: Color(0xFF0F7A5A),
                                    width: 1,
                                  ),
                                ),
                                child: SafeArea(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.center,
                                    children: [
                                      SizedBox(height: 40),
                                      Padding(
                                        padding: EdgeInsets.symmetric(
                                            horizontal: 24),
                                        child: Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.center,
                                          children: [
                                            Container(
                                              width: 100,
                                              height: 100,
                                              decoration: BoxDecoration(
                                                shape: BoxShape.circle,
                                                color: Color(0xFFF5E9D0)
                                                    .withOpacity(0.2),
                                                border: Border.all(
                                                  color: Color(0xFFF5E9D0),
                                                  width: 2,
                                                ),
                                              ),
                                              child: Icon(
                                                Icons.person,
                                                color: Color(0xFFF5E9D0),
                                                size: 60,
                                              ),
                                            ),
                                            SizedBox(height: 10),
                                            Text(
                                              'Username',
                                              style: TextStyle(
                                                fontSize: 18,
                                                fontWeight: FontWeight.bold,
                                                color: Color(0xFFF5E9D0),
                                                fontFamily: 'Montserrat',
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                      SizedBox(height: 40),
                                      _buildEnhancedMenuButton(Icons.people,
                                          'Friends', _navigateToFriends),
                                      _buildEnhancedMenuButton(Icons.settings,
                                          'Settings', () => _closeSideMenu()),
                                      _buildEnhancedMenuButton(Icons.favorite,
                                          'Favorites', () => _closeSideMenu()),
                                      _buildEnhancedMenuButton(Icons.history,
                                          'History', () => _closeSideMenu()),
                                      Spacer(),
                                      _buildEnhancedMenuButton(
                                          Icons.logout, 'Sign Out', _signOut,
                                          isDestructive: true),
                                      SizedBox(height: 40),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

          // Bottom Panel for Route Details - shows automatically with single route
          if (_isBottomPanelOpen && _selectedRoute != null)
            SlideTransition(
              position: _bottomPanelAnimation,
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Container(
                  width: double.infinity,
                  constraints: BoxConstraints(
                    maxHeight: 230, // Increased height to fit Go button better
                    minHeight: 210, // Increased minimum height
                  ),
                  child: ClipRRect(
                    borderRadius:
                        BorderRadius.vertical(top: Radius.circular(24)),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaX: 25, sigmaY: 25),
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              Color(0xFF06332E).withOpacity(0.95),
                              Color(0xFF0B664E).withOpacity(0.95),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                          border: Border.all(
                            color: Color(0xFF0F7A5A),
                            width: 1,
                          ),
                        ),
                        child: SafeArea(
                          child: Padding(
                            padding: EdgeInsets.all(20),
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  children: [
                                    Expanded(
                                      child: Text(
                                        _selectedRoute!.name,
                                        style: TextStyle(
                                          fontSize: 22,
                                          fontWeight: FontWeight.bold,
                                          color: Color(0xFFF5E9D0),
                                          fontFamily: 'Montserrat',
                                        ),
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                    ),
                                    GestureDetector(
                                      onTap: _closeBottomPanel,
                                      child: Icon(Icons.close,
                                          color: Color(0xFFF5E9D0)),
                                    ),
                                  ],
                                ),
                                SizedBox(height: 12),
                                Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceAround,
                                  children: [
                                    _buildRouteDetail(Icons.access_time,
                                        _selectedRoute!.duration),
                                    _buildRouteDetail(Icons.straighten,
                                        _selectedRoute!.distance),
                                    _buildRouteDetail(Icons.attach_money,
                                        _selectedRoute!.cost),
                                  ],
                                ),
                                SizedBox(height: 16),
                                Center(
                                  child: _EnhancedGoButton(onTap: _onGo),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),

          // Enhanced Favorite Location Dialog with green gradient Add button
          if (_showFavoriteDialog)
            Container(
              color: Colors.black.withOpacity(0.5),
              child: Center(
                child: AnimatedBuilder(
                  animation: _favoriteDialogController,
                  builder: (context, child) => Transform.scale(
                    scale: _favoriteDialogScale.value,
                    child: Opacity(
                      opacity: _favoriteDialogOpacity.value,
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(24),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
                          child: Container(
                            width: 320,
                            padding: EdgeInsets.all(24),
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [
                                  Color(0xFFF5E9D0).withOpacity(0.95),
                                  Color(0xFFE8D5B7).withOpacity(0.95),
                                ],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              borderRadius: BorderRadius.circular(24),
                              border: Border.all(
                                color: Color(0xFF06332E).withOpacity(0.3),
                                width: 2,
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.2),
                                  blurRadius: 20,
                                  offset: Offset(0, 10),
                                ),
                              ],
                            ),
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      'Name the Location',
                                      style: TextStyle(
                                        fontSize: 20,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF06332E),
                                        fontFamily: 'Montserrat',
                                      ),
                                    ),
                                    GestureDetector(
                                      onTap: _closeFavoriteDialog,
                                      child: Container(
                                        padding: EdgeInsets.all(4),
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: Color(0xFF06332E)
                                              .withOpacity(0.1),
                                        ),
                                        child: Icon(Icons.close,
                                            color: Color(0xFF06332E)),
                                      ),
                                    ),
                                  ],
                                ),
                                SizedBox(height: 20),
                                TextField(
                                  controller: _favoriteNameController,
                                  focusNode: _favoriteNameFocusNode,
                                  style: TextStyle(
                                    color: Color(0xFF06332E),
                                    fontFamily: 'Montserrat',
                                    fontWeight: FontWeight.w500,
                                  ),
                                  decoration: InputDecoration(
                                    hintText: 'Enter location name...',
                                    hintStyle: TextStyle(
                                      color: Color(0xFF06332E).withOpacity(0.6),
                                    ),
                                    filled: true,
                                    fillColor: Colors.white.withOpacity(0.7),
                                    border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(16),
                                      borderSide: BorderSide(
                                        color:
                                            Color(0xFF06332E).withOpacity(0.3),
                                      ),
                                    ),
                                    focusedBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(16),
                                      borderSide: BorderSide(
                                        color: Color(0xFF06332E),
                                        width: 2,
                                      ),
                                    ),
                                  ),
                                ),
                                SizedBox(height: 20),
                                // Enhanced Add button with green gradient
                                GestureDetector(
                                  onTap: _addFavoriteLocation,
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.circular(20),
                                    child: BackdropFilter(
                                      filter: ImageFilter.blur(
                                          sigmaX: 10, sigmaY: 10),
                                      child: Container(
                                        width: double.infinity,
                                        padding:
                                            EdgeInsets.symmetric(vertical: 16),
                                        decoration: BoxDecoration(
                                          gradient: LinearGradient(
                                            colors: [
                                              Color(0xFF06332E).withOpacity(
                                                  0.9), // Green gradient
                                              Color(0xFF0B664E)
                                                  .withOpacity(0.9),
                                            ],
                                            begin: Alignment.topLeft,
                                            end: Alignment.bottomRight,
                                          ),
                                          borderRadius:
                                              BorderRadius.circular(20),
                                          border: Border.all(
                                            color: Color(0xFF0F7A5A),
                                            width: 1.5,
                                          ),
                                          boxShadow: [
                                            BoxShadow(
                                              color:
                                                  Colors.black.withOpacity(0.2),
                                              blurRadius: 8,
                                              offset: Offset(0, 4),
                                            ),
                                          ],
                                        ),
                                        child: Center(
                                          child: Text(
                                            'Add',
                                            style: TextStyle(
                                              color: Color(
                                                  0xFFF5E9D0), // Light text on green
                                              fontSize: 18,
                                              fontWeight: FontWeight.bold,
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
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),

          // Offline mode banner
          if (offlineMode)
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: ClipRRect(
                borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
                  child: Container(
                    color: Color(0xFFF5E9D0).withOpacity(0.92),
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    child: const Center(
                      child: Text(
                        'You are in offline mode. Some features may be limited.',
                        style: TextStyle(
                          color: Color(0xFF8F8262),
                          fontSize: 15,
                          fontFamily: 'Montserrat',
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),

          // Enhanced notification system
          if (_showNotification)
            Positioned(
              top: 0,
              left: 0,
              right: 0,
              child: Material(
                color: Colors.transparent,
                elevation: 20,
                child: SlideTransition(
                  position: _notificationSlideAnimation,
                  child: AnimatedBuilder(
                    animation: _notificationOpacityAnimation,
                    builder: (context, child) => Opacity(
                      opacity: _notificationOpacityAnimation.value,
                      child: SafeArea(
                        child: Container(
                          margin:
                              EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(20),
                            child: BackdropFilter(
                              filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
                              child: Container(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 20, vertical: 16),
                                decoration: BoxDecoration(
                                  gradient: LinearGradient(
                                    colors: [
                                      _notificationColor.withOpacity(0.95),
                                      _notificationColor.withOpacity(0.85),
                                    ],
                                    begin: Alignment.topLeft,
                                    end: Alignment.bottomRight,
                                  ),
                                  borderRadius: BorderRadius.circular(20),
                                  border: Border.all(
                                    color: _notificationColor.withOpacity(0.3),
                                    width: 1.5,
                                  ),
                                  boxShadow: [
                                    BoxShadow(
                                      color: Colors.black.withOpacity(0.25),
                                      blurRadius: 25,
                                      offset: Offset(0, 12),
                                    ),
                                  ],
                                ),
                                child: Row(
                                  children: [
                                    Icon(_notificationIcon,
                                        color: Colors.white, size: 24),
                                    SizedBox(width: 12),
                                    Expanded(
                                      child: Text(
                                        _notificationText,
                                        style: TextStyle(
                                          color: Colors.white,
                                          fontSize: 14,
                                          fontWeight: FontWeight.w500,
                                          fontFamily: 'Montserrat',
                                        ),
                                      ),
                                    ),
                                    GestureDetector(
                                      onTap: _hideCustomNotification,
                                      child: Container(
                                        padding: EdgeInsets.all(4),
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: Colors.white.withOpacity(0.2),
                                        ),
                                        child: Icon(Icons.close,
                                            color:
                                                Colors.white.withOpacity(0.8),
                                            size: 16),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
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

  IconData _getLocationIcon(String locationName) {
    switch (locationName.toLowerCase()) {
      case 'home':
        return Icons.home;
      case 'work':
        return Icons.work;
      case 'school':
        return Icons.school;
      case 'university':
        return Icons.school;
      case 'hospital':
        return Icons.local_hospital;
      case 'mall':
        return Icons.shopping_cart;
      case 'airport':
        return Icons.flight;
      case 'park':
        return Icons.park;
      case 'restaurant':
        return Icons.restaurant;
      case 'hotel':
        return Icons.hotel;
      default:
        return Icons.location_on;
    }
  }

  Widget _buildRouteDetail(IconData icon, String text) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          padding: EdgeInsets.all(10),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Color(0xFFF5E9D0).withOpacity(0.2),
            boxShadow: [
              BoxShadow(
                color: Color(0xFFF5E9D0).withOpacity(0.1),
                blurRadius: 4,
                spreadRadius: 1,
              ),
            ],
          ),
          child: Icon(icon, color: Color(0xFFF5E9D0), size: 22),
        ),
        SizedBox(height: 6),
        Container(
          width: 80, // Fixed width for text container
          child: Text(
            text,
            style: TextStyle(
              color: Color(0xFFF5E9D0),
              fontSize: 14,
              fontWeight: FontWeight.w600,
              fontFamily: 'Montserrat',
              shadows: [
                Shadow(
                  blurRadius: 2.0,
                  color: Colors.black.withOpacity(0.3),
                  offset: Offset(0, 1),
                ),
              ],
            ),
            overflow: TextOverflow.ellipsis,
            textAlign: TextAlign.center,
            maxLines: 1,
          ),
        ),
      ],
    );
  }

  Widget _buildEnhancedMenuButton(
      IconData icon, String title, VoidCallback onTap,
      {bool isDestructive = false}) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
          child: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: isDestructive
                    ? [
                        Colors.red.withOpacity(0.2),
                        Colors.red.withOpacity(0.1),
                      ]
                    : [
                        Colors.white.withOpacity(0.15),
                        Colors.white.withOpacity(0.05),
                      ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: isDestructive
                    ? Colors.red.withOpacity(0.3)
                    : Color(0xFFF5E9D0).withOpacity(0.2),
                width: 1,
              ),
            ),
            child: ListTile(
              contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              leading: Container(
                padding: EdgeInsets.all(8),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: isDestructive
                      ? Colors.red.withOpacity(0.2)
                      : Color(0xFFF5E9D0).withOpacity(0.2),
                ),
                child: Icon(
                  icon,
                  color:
                      isDestructive ? Colors.red.shade300 : Color(0xFFF5E9D0),
                  size: 24,
                ),
              ),
              title: Text(
                title,
                style: TextStyle(
                  color:
                      isDestructive ? Colors.red.shade300 : Color(0xFFF5E9D0),
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Montserrat',
                ),
              ),
              trailing: Icon(
                Icons.arrow_forward_ios,
                color: isDestructive
                    ? Colors.red.shade300
                    : Color(0xFFF5E9D0).withOpacity(0.6),
                size: 16,
              ),
              onTap: onTap,
            ),
          ),
        ),
      ),
    );
  }
}

// Updated Pin component for single route
class _PinWithAnimatedButtons extends StatefulWidget {
  final String? selected;
  final void Function(String) onSelect;
  final VoidCallback onGo;
  final VoidCallback onMakeFavorite;
  final RouteData? selectedRoute;
  final bool isTransitioning;
  final Animation<double> transitionAnimation;

  const _PinWithAnimatedButtons({
    required this.selected,
    required this.onSelect,
    required this.onGo,
    required this.onMakeFavorite,
    this.selectedRoute,
    required this.isTransitioning,
    required this.transitionAnimation,
    Key? key,
  }) : super(key: key);

  @override
  State<_PinWithAnimatedButtons> createState() =>
      _PinWithAnimatedButtonsState();
}

class _PinWithAnimatedButtonsState extends State<_PinWithAnimatedButtons>
    with TickerProviderStateMixin {
  late final AnimationController _controller;
  late final AnimationController _pinController;
  late final Animation<double> _pinOpacity;
  late final Animation<double> _pinScale;
  late final Animation<double> _buttonsOpacity;
  late final Animation<double> _buttonsScale;
  late final Animation<Offset> _fewestOffset;
  late final Animation<Offset> _fastestOffset;
  late final Animation<Offset> _cheapestOffset;
  late final Animation<double> _favoriteOpacity;
  late final Animation<double> _favoriteScale;

  @override
  void initState() {
    super.initState();
    _initAnimations();
  }

  void _initAnimations() {
    _pinController = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 150));

    _controller = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 600));

    _pinOpacity = Tween<double>(begin: 0, end: 1).animate(
        CurvedAnimation(parent: _pinController, curve: Curves.easeInOut));

    _pinScale = Tween<double>(begin: 0.3, end: 1).animate(
        CurvedAnimation(parent: _pinController, curve: Curves.elasticOut));

    _favoriteOpacity = Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.1, 0.4, curve: Curves.easeOut)));

    _favoriteScale = Tween<double>(begin: 0.1, end: 1).animate(CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.1, 0.5, curve: Curves.elasticOut)));

    _buttonsOpacity = Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.3, 0.7, curve: Curves.easeOut)));

    _buttonsScale = Tween<double>(begin: 0.1, end: 1).animate(CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.4, 0.9, curve: Curves.elasticOut)));

    _fewestOffset =
        Tween<Offset>(begin: const Offset(0, 0), end: const Offset(-1.2, -0.15))
            .animate(CurvedAnimation(
                parent: _controller,
                curve: const Interval(0.2, 0.8, curve: Curves.easeOutCubic)));

    _fastestOffset =
        Tween<Offset>(begin: const Offset(0, 0), end: const Offset(0, -0.3))
            .animate(CurvedAnimation(
                parent: _controller,
                curve: const Interval(0.3, 0.9, curve: Curves.easeOutCubic)));

    _cheapestOffset =
        Tween<Offset>(begin: const Offset(0, 0), end: const Offset(1.2, -0.15))
            .animate(CurvedAnimation(
                parent: _controller,
                curve: const Interval(0.2, 0.8, curve: Curves.easeOutCubic)));
  }

  void resetAnimation() {
    _controller.stop();
    _pinController.stop();
    _controller.reset();
    _pinController.reset();
  }

  void playForward() {
    _pinController.forward(from: 0).then((_) {
      Future.delayed(const Duration(milliseconds: 50), () {
        _controller.forward(from: 0);
      });
    });
  }

  void playReverse({VoidCallback? onComplete}) {
    _controller.reverse().then((_) {
      _pinController.reverse().then((_) {
        if (onComplete != null) onComplete();
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _pinController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Favorite button above pin
          AnimatedBuilder(
            animation: _controller,
            builder: (context, child) => Transform.scale(
              scale: _favoriteScale.value,
              child: Opacity(
                opacity: _favoriteOpacity.value,
                child: Container(
                  margin: EdgeInsets.only(bottom: 8),
                  child: GestureDetector(
                    onTap: widget.onMakeFavorite,
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(20),
                      child: BackdropFilter(
                        filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
                        child: Container(
                          padding:
                              EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Color(0xFFE8D5B7).withOpacity(0.9),
                                Color(0xFFF5E9D0).withOpacity(0.9),
                              ],
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                            ),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(
                              color: Color(0xFF06332E).withOpacity(0.3),
                              width: 1.5,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.1),
                                blurRadius: 8,
                                offset: Offset(0, 4),
                              ),
                            ],
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.favorite_border,
                                  color: Color(0xFF06332E), size: 16),
                              SizedBox(width: 6),
                              Text(
                                'Add to Favorites',
                                style: TextStyle(
                                  color: Color(0xFF06332E),
                                  fontSize: 12,
                                  fontWeight: FontWeight.w600,
                                  fontFamily: 'Montserrat',
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Pin
          AnimatedBuilder(
            animation: _pinController,
            builder: (context, child) => Transform.scale(
              scale: _pinScale.value,
              child: Opacity(
                opacity: _pinOpacity.value,
                child: Container(
                  alignment: Alignment.bottomCenter,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      Positioned(
                        top: 2,
                        child: Container(
                          width: 48,
                          height: 48,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: Colors.black.withOpacity(0.15),
                          ),
                        ),
                      ),
                      const Icon(
                        Icons.location_on,
                        color: Colors.red,
                        size: 48,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 4),

          // Route option buttons - only show if no route is selected yet
          if (widget.selectedRoute == null)
            AnimatedBuilder(
              animation: widget.isTransitioning
                  ? widget.transitionAnimation
                  : _controller,
              builder: (context, child) {
                final opacity = widget.isTransitioning
                    ? (1.0 - widget.transitionAnimation.value) *
                        _buttonsOpacity.value
                    : _buttonsOpacity.value;

                return Opacity(
                  opacity: opacity,
                  child: Transform.scale(
                    scale: _buttonsScale.value,
                    child: SizedBox(
                      width: 350,
                      height: 70,
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          AnimatedBuilder(
                            animation: _fewestOffset,
                            builder: (context, child) => Transform.translate(
                              offset: Offset(_fewestOffset.value.dx * 80,
                                  _fewestOffset.value.dy * 80),
                              child: Container(
                                width: 110,
                                height: 55,
                                alignment: Alignment.center,
                                child: _RouteOptionButton(
                                  label: 'Fewest',
                                  selected: widget.selected == 'fewest',
                                  onTap: () => widget.onSelect('fewest'),
                                  width: 85,
                                ),
                              ),
                            ),
                          ),
                          AnimatedBuilder(
                            animation: _fastestOffset,
                            builder: (context, child) => Transform.translate(
                              offset: Offset(_fastestOffset.value.dx * 80,
                                  _fastestOffset.value.dy * 80),
                              child: Container(
                                width: 110,
                                height: 55,
                                alignment: Alignment.center,
                                child: _RouteOptionButton(
                                  label: 'Fastest',
                                  selected: widget.selected == 'fastest',
                                  onTap: () => widget.onSelect('fastest'),
                                  width: 85,
                                ),
                              ),
                            ),
                          ),
                          AnimatedBuilder(
                            animation: _cheapestOffset,
                            builder: (context, child) => Transform.translate(
                              offset: Offset(_cheapestOffset.value.dx * 80,
                                  _cheapestOffset.value.dy * 80),
                              child: Container(
                                width: 110,
                                height: 55,
                                alignment: Alignment.center,
                                child: _RouteOptionButton(
                                  label: 'Cheapest',
                                  selected: widget.selected == 'cheapest',
                                  onTap: () => widget.onSelect('cheapest'),
                                  width: 85,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
        ],
      ),
    );
  }
}

class _RouteOptionButton extends StatefulWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;
  final double width;

  const _RouteOptionButton({
    required this.label,
    required this.selected,
    required this.onTap,
    this.width = 80,
    Key? key,
  }) : super(key: key);

  @override
  State<_RouteOptionButton> createState() => _RouteOptionButtonState();
}

class _RouteOptionButtonState extends State<_RouteOptionButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _tapController;
  late Animation<double> _tapAnimation;

  @override
  void initState() {
    super.initState();
    _tapController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 150),
    );
    _tapAnimation = Tween<double>(begin: 1.0, end: 0.92).animate(
      CurvedAnimation(parent: _tapController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _tapController.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails details) {
    _tapController.forward();
  }

  void _onTapUp(TapUpDetails details) {
    _tapController.reverse();
    widget.onTap();
  }

  void _onTapCancel() {
    _tapController.reverse();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _tapAnimation,
      builder: (context, child) => Transform.scale(
        scale: _tapAnimation.value,
        child: GestureDetector(
          onTapDown: _onTapDown,
          onTapUp: _onTapUp,
          onTapCancel: _onTapCancel,
          behavior: HitTestBehavior.opaque,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
                width: widget.selected ? widget.width + 16 : widget.width,
                height: widget.selected ? 42 : 36,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: widget.selected
                        ? [
                            Color(0xFF0B664E).withOpacity(0.85),
                            Color(0xFF06332E).withOpacity(0.85),
                          ]
                        : [
                            Color(0xFF06332E).withOpacity(0.75),
                            Color(0xFF0B664E).withOpacity(0.75),
                          ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: Color(0xFF0F7A5A),
                    width: 1.5,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.2),
                      blurRadius: widget.selected ? 8 : 4,
                      offset: Offset(0, widget.selected ? 4 : 2),
                    ),
                  ],
                ),
                child: Text(
                  widget.label,
                  style: TextStyle(
                    color: Color(0xFFF5E9D0),
                    fontWeight: FontWeight.bold,
                    fontSize: widget.selected ? 16 : 14,
                    fontFamily: 'Montserrat',
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _EnhancedGoButton extends StatefulWidget {
  final VoidCallback onTap;
  const _EnhancedGoButton({required this.onTap, Key? key}) : super(key: key);

  @override
  State<_EnhancedGoButton> createState() => _EnhancedGoButtonState();
}

class _EnhancedGoButtonState extends State<_EnhancedGoButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _hoverController;
  late Animation<double> _scaleAnimation;
  late Animation<double> _glowAnimation;

  @override
  void initState() {
    super.initState();
    _hoverController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 200),
    );

    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.05).animate(
      CurvedAnimation(parent: _hoverController, curve: Curves.easeInOut),
    );

    _glowAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _hoverController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _hoverController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _hoverController,
      builder: (context, child) => Transform.scale(
        scale: _scaleAnimation.value,
        child: GestureDetector(
          onTapDown: (_) => _hoverController.forward(),
          onTapUp: (_) {
            _hoverController.reverse();
            widget.onTap();
          },
          onTapCancel: () => _hoverController.reverse(),
          behavior: HitTestBehavior.opaque,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(25),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
              child: Container(
                width: 150,
                height: 50,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Color(0xFFF5E9D0).withOpacity(0.95),
                      Color(0xFFE8D5B7).withOpacity(0.95),
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(25),
                  border: Border.all(
                    color: Color(0xFF06332E).withOpacity(0.3),
                    width: 2,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.2),
                      blurRadius: 12,
                      offset: Offset(0, 6),
                    ),
                    if (_glowAnimation.value > 0)
                      BoxShadow(
                        color: Color(0xFFF5E9D0)
                            .withOpacity(_glowAnimation.value * 0.5),
                        blurRadius: 16,
                        offset: Offset(0, 0),
                        spreadRadius: 1,
                      ),
                  ],
                ),
                child: Stack(
                  children: [
                    // Subtle animated gradient overlay
                    if (_glowAnimation.value > 0)
                      Positioned.fill(
                        child: Opacity(
                          opacity: _glowAnimation.value * 0.3,
                          child: Container(
                            decoration: BoxDecoration(
                              gradient: RadialGradient(
                                colors: [
                                  Colors.white.withOpacity(0.7),
                                  Colors.white.withOpacity(0.0),
                                ],
                                center: Alignment.center,
                                radius: 0.8,
                              ),
                            ),
                          ),
                        ),
                      ),
                    // Button content
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.directions,
                            color: Color(0xFF06332E), size: 24),
                        SizedBox(width: 10),
                        Text(
                          'Go',
                          style: TextStyle(
                            color: Color(0xFF06332E),
                            fontWeight: FontWeight.bold,
                            fontSize: 18, // Slightly larger text
                            fontFamily: 'Montserrat',
                          ),
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
    );
  }
}

// Data classes
class SearchLocationData {
  final String name;
  final LatLng location;

  SearchLocationData(this.name, this.location);
}

class RouteData {
  final String name;
  final String duration;
  final String distance;
  final String cost;
  final List<LatLng> points;
  final Color color;

  RouteData({
    required this.name,
    required this.duration,
    required this.distance,
    required this.cost,
    required this.points,
    required this.color,
  });
}

class Destination {
  final String name;
  final LatLng location;

  Destination(this.name, this.location);
}

class SearchDestinationScreen extends StatelessWidget {
  final String? initialQuery;

  const SearchDestinationScreen({this.initialQuery, Key? key})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Search Destinations')),
      body: Center(child: Text('Search implementation here')),
    );
  }
}

class RouteOptionsScreen extends StatelessWidget {
  final LatLng start;
  final Destination destination;
  final String? initialFilter;
  final bool offlineMode;

  const RouteOptionsScreen({
    required this.start,
    required this.destination,
    this.initialFilter,
    this.offlineMode = false,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Route Options')),
      body: Center(child: Text('Route options implementation here')),
    );
  }
}
