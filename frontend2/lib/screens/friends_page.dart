import 'package:flutter/material.dart';
import 'dart:ui';
import 'dart:math';
import 'package:latlong2/latlong.dart';

class FriendsPage extends StatefulWidget {
  @override
  State<FriendsPage> createState() => _FriendsPageState();
}

class _FriendsPageState extends State<FriendsPage> with TickerProviderStateMixin {
  late TabController _tabController;
  final TextEditingController _searchController = TextEditingController();
  final FocusNode _searchFocusNode = FocusNode();

  // Mock friends data
  final List<Friend> _friends = [
    Friend('Alice Johnson', 'https://placeholder.svg?height=50&width=50&text=AJ', false),
    Friend('Bob Smith', 'https://placeholder.svg?height=50&width=50&text=BS', true),
    Friend('Carol Davis', 'https://placeholder.svg?height=50&width=50&text=CD', false),
    Friend('David Wilson', 'https://placeholder.svg?height=50&width=50&text=DW', true),
    Friend('Emma Brown', 'https://placeholder.svg?height=50&width=50&text=EB', false),
  ];

  List<Friend> get _filteredFriends {
    if (_searchController.text.isEmpty) {
      return _friends;
    }
    return _friends
        .where((friend) => friend.name.toLowerCase().contains(_searchController.text.toLowerCase()))
        .toList();
  }

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _searchController.addListener(() {
      setState(() {});
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    _searchController.dispose();
    _searchFocusNode.dispose();
    super.dispose();
  }

  void _toggleFollow(int index) {
    setState(() {
      Friend friend;
      if (_searchController.text.isEmpty) {
        friend = _friends[index];
        _friends[index].isFollowing = !_friends[index].isFollowing;
      } else {
        friend = _filteredFriends[index];
        final originalIndex = _friends.indexOf(friend);
        _friends[originalIndex].isFollowing = !_friends[originalIndex].isFollowing;
      }
      
      // If now located (following), return to map with this friend's location
      if (friend.isFollowing) {
        // Return to map and show friend's location
        Navigator.pop(context, friend);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xFF06332E),
              Color(0xFF0B664E),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Header
              Padding(
                padding: EdgeInsets.all(20),
                child: Row(
                  children: [
                    GestureDetector(
                      onTap: () => Navigator.pop(context),
                      child: Container(
                        padding: EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: Color(0xFFF5E9D0).withOpacity(0.2),
                        ),
                        child: Icon(
                          Icons.arrow_back,
                          color: Color(0xFFF5E9D0),
                          size: 24,
                        ),
                      ),
                    ),
                    SizedBox(width: 16),
                    Text(
                      'Friends',
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFF5E9D0),
                        fontFamily: 'Montserrat',
                      ),
                    ),
                  ],
                ),
              ),

              // Tab Bar
              Container(
                margin: EdgeInsets.symmetric(horizontal: 20),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(25),
                  color: Color(0xFFF5E9D0).withOpacity(0.1),
                  border: Border.all(
                    color: Color(0xFFF5E9D0).withOpacity(0.3),
                    width: 1.5,
                  ),
                ),
                child: TabBar(
                  controller: _tabController,
                  indicator: BoxDecoration(
                    borderRadius: BorderRadius.circular(25),
                    gradient: LinearGradient(
                      colors: [
                        Color(0xFFF5E9D0).withOpacity(0.9),
                        Color(0xFFE8D5B7).withOpacity(0.9),
                      ],
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Color(0xFF06332E).withOpacity(0.2),
                        blurRadius: 4,
                        offset: Offset(0, 2),
                      ),
                    ],
                  ),
                  labelColor: Color(0xFF06332E),
                  unselectedLabelColor: Color(0xFFF5E9D0),
                  labelStyle: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontFamily: 'Montserrat',
                  ),
                  tabs: [
                    Tab(text: 'Friend List'),
                    Tab(text: 'Add'),
                  ],
                ),
              ),

              SizedBox(height: 20),

              // Tab Views
              Expanded(
                child: TabBarView(
                  controller: _tabController,
                  children: [
                    // Friend List Tab
                    _buildFriendsList(),

                    // Add Friends Tab
                    _buildAddFriends(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFriendsList() {
    return Column(
      children: [
        // Search bar for friends list
        Container(
          margin: EdgeInsets.symmetric(horizontal: 20),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                decoration: BoxDecoration(
                  color: Color(0xFFF5E9D0).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: Color(0xFFF5E9D0).withOpacity(0.3),
                    width: 1,
                  ),
                ),
                child: Row(
                  children: [
                    Icon(Icons.search, color: Color(0xFFF5E9D0)),
                    SizedBox(width: 12),
                    Expanded(
                      child: TextField(
                        controller: _searchController,
                        focusNode: _searchFocusNode,
                        style: TextStyle(
                          color: Color(0xFFF5E9D0),
                          fontFamily: 'Montserrat',
                        ),
                        decoration: InputDecoration(
                          hintText: 'Search friends...',
                          hintStyle: TextStyle(
                            color: Color(0xFFF5E9D0).withOpacity(0.6),
                          ),
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),

        SizedBox(height: 20),

        // Friends List
        Expanded(
          child: ListView.builder(
            padding: EdgeInsets.symmetric(horizontal: 20),
            itemCount: _filteredFriends.length,
            itemBuilder: (context, index) {
              final friend = _filteredFriends[index];
              return Container(
                margin: EdgeInsets.only(bottom: 12),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(16),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                    child: Container(
                      padding: EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Color(0xFFF5E9D0).withOpacity(0.1),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: Color(0xFFF5E9D0).withOpacity(0.2),
                          width: 1,
                        ),
                      ),
                      child: Row(
                        children: [
                          // Profile Picture
                          Container(
                            width: 50,
                            height: 50,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: Color(0xFFF5E9D0),
                                width: 2,
                              ),
                            ),
                            child: ClipOval(
                              child: Image.network(
                                friend.profilePicture,
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) {
                                  return Container(
                                    color: Color(0xFFF5E9D0).withOpacity(0.3),
                                    child: Icon(
                                      Icons.person,
                                      color: Color(0xFFF5E9D0),
                                      size: 30,
                                    ),
                                  );
                                },
                              ),
                            ),
                          ),

                          SizedBox(width: 16),

                          // Name
                          Expanded(
                            child: Text(
                              friend.name,
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color: Color(0xFFF5E9D0),
                                fontFamily: 'Montserrat',
                              ),
                            ),
                          ),

                          // Locate Button
                          GestureDetector(
                            onTap: () => _toggleFollow(index),
                            child: Container(
                              padding: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                              decoration: BoxDecoration(
                                gradient: friend.isFollowing
                                    ? LinearGradient(
                                  colors: [
                                    Colors.grey.withOpacity(0.8),
                                    Colors.grey.withOpacity(0.6),
                                  ],
                                )
                                    : LinearGradient(
                                  colors: [
                                    Color(0xFFF5E9D0).withOpacity(0.9),
                                    Color(0xFFE8D5B7).withOpacity(0.9),
                                  ],
                                ),
                                borderRadius: BorderRadius.circular(20),
                                border: Border.all(
                                  color: friend.isFollowing
                                      ? Colors.grey.withOpacity(0.5)
                                      : Color(0xFF06332E).withOpacity(0.3),
                                  width: 1,
                                ),
                              ),
                              child: Text(
                                friend.isFollowing ? 'Located' : 'Locate',
                                style: TextStyle(
                                  color: friend.isFollowing
                                      ? Colors.white
                                      : Color(0xFF06332E),
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                  fontFamily: 'Montserrat',
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildAddFriends() {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        children: [
          // Search bar for adding friends
          ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                decoration: BoxDecoration(
                  color: Color(0xFFF5E9D0).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: Color(0xFFF5E9D0).withOpacity(0.3),
                    width: 1,
                  ),
                ),
                child: Row(
                  children: [
                    Icon(Icons.search, color: Color(0xFFF5E9D0)),
                    SizedBox(width: 12),
                    Expanded(
                      child: TextField(
                        style: TextStyle(
                          color: Color(0xFFF5E9D0),
                          fontFamily: 'Montserrat',
                        ),
                        decoration: InputDecoration(
                          hintText: 'Search for new friends...',
                          hintStyle: TextStyle(
                            color: Color(0xFFF5E9D0).withOpacity(0.6),
                          ),
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            Color(0xFFF5E9D0).withOpacity(0.9),
                            Color(0xFFE8D5B7).withOpacity(0.9),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(15),
                      ),
                      child: Text(
                        'Search',
                        style: TextStyle(
                          color: Color(0xFF06332E),
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                          fontFamily: 'Montserrat',
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          SizedBox(height: 40),

          // Placeholder content
          Expanded(
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    padding: EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: Color(0xFFF5E9D0).withOpacity(0.2),
                    ),
                    child: Icon(
                      Icons.person_add,
                      size: 48,
                      color: Color(0xFFF5E9D0),
                    ),
                  ),
                  SizedBox(height: 20),
                  Text(
                    'Find New Friends',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFFF5E9D0),
                      fontFamily: 'Montserrat',
                    ),
                  ),
                  SizedBox(height: 12),
                  Text(
                    'Search for friends by name or username\nto connect and share your journeys',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 16,
                      color: Color(0xFFF5E9D0).withOpacity(0.8),
                      fontFamily: 'Montserrat',
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class Friend {
  final String name;
  final String profilePicture;
  bool isFollowing;
  // Random location in Damascus for demonstration
  final LatLng location;

  Friend(this.name, this.profilePicture, this.isFollowing)
      : location = LatLng(
          33.5138 + (Random().nextDouble() - 0.5) * 0.05,
          36.2765 + (Random().nextDouble() - 0.5) * 0.05,
        );
}
