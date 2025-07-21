import 'dart:ui';
import 'package:flutter/material.dart';

class TripRatingScreen extends StatefulWidget {
  const TripRatingScreen({Key? key}) : super(key: key);

  @override
  State<TripRatingScreen> createState() => _TripRatingScreenState();
}

class _TripRatingScreenState extends State<TripRatingScreen> {
  int _rating = 0;
  final TextEditingController _notesController = TextEditingController();

  void _submit() {
    // For demo, just pop to root
    Navigator.of(context).popUntil((route) => route.isFirst);
  }

  void _skip() {
    Navigator.of(context).popUntil((route) => route.isFirst);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Rate Your Trip'),
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
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(32),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 16, sigmaY: 16),
                child: Container(
                  constraints: const BoxConstraints(
                    minWidth: 350,
                    maxWidth: 420,
                  ),
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 32),
                  decoration: const BoxDecoration(
                    color: Color(0x2EFFFFFF),
                    borderRadius: BorderRadius.all(Radius.circular(32)),
                    border: Border.fromBorderSide(BorderSide(color: Color(0x4DFFFFFF), width: 1.2)),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 12,
                        offset: Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const SizedBox(height: 24),
                      const Text('How was your trip?', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20, fontFamily: 'Montserrat', color: Color(0xFF06332E))),
                      const SizedBox(height: 24),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: List.generate(5, (i) => IconButton(
                          icon: _rating > i
                              ? const Icon(Icons.star, color: Colors.amber, size: 36)
                              : const Icon(Icons.star_border, color: Colors.amber, size: 36),
                          onPressed: () {
                            setState(() {
                              _rating = i + 1;
                            });
                          },
                        )),
                      ),
                      const SizedBox(height: 24),
                      TextField(
                        controller: _notesController,
                        minLines: 2,
                        maxLines: 4,
                        style: const TextStyle(fontFamily: 'Montserrat', color: Color(0xFF06332E)),
                        decoration: const InputDecoration(
                          labelText: 'Add notes (optional)',
                          labelStyle: TextStyle(fontFamily: 'Montserrat', color: Color(0xFF8F8262)),
                          border: OutlineInputBorder(borderRadius: BorderRadius.all(Radius.circular(16))),
                        ),
                      ),
                      const SizedBox(height: 32),
                      Row(
                        children: [
                          Expanded(
                            child: OutlinedButton(
                              onPressed: _skip,
                              style: OutlinedButton.styleFrom(
                                side: const BorderSide(color: Color(0xFF06332E), width: 2),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                                padding: const EdgeInsets.symmetric(vertical: 16),
                                foregroundColor: const Color(0xFF06332E),
                              ),
                              child: const Text('Skip', style: TextStyle(fontSize: 16, color: Color(0xFF06332E), fontFamily: 'Montserrat', fontWeight: FontWeight.bold)),
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: ElevatedButton(
                              onPressed: _submit,
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
                                    'Submit',
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
                      const SizedBox(height: 24),
                    ],
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