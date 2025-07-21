from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .base import Base
import datetime
import enum

# Enum for friendship status
class FriendshipStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# Enum for location sharing status
class LocationSharingStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer)
    operating_hours = Column(String)
    # علاقات
    stops = relationship('RouteStop', back_populates='route')
    paths = relationship('RoutePath', back_populates='route')
    feedbacks = relationship('Feedback', back_populates='route')
    complaints = relationship('Complaint', back_populates='route')

class Stop(Base):
    __tablename__ = 'stops'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    geom = Column(Geometry('POINT'))
    # علاقات
    routes = relationship('RouteStop', back_populates='stop')

class RouteStop(Base):
    __tablename__ = 'route_stops'
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    stop_id = Column(Integer, ForeignKey('stops.id'))
    stop_order = Column(Integer)
    # علاقات
    route = relationship('Route', back_populates='stops')
    stop = relationship('Stop', back_populates='routes')

class RoutePath(Base):
    __tablename__ = 'route_paths'
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    geom = Column(Geometry('POINT'))
    point_order = Column(Integer)
    # علاقات
    route = relationship('Route', back_populates='paths')

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    rating = Column(Integer)
    comment = Column(Text)
    route_id = Column(Integer, ForeignKey('routes.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    # علاقات
    route = relationship('Route', back_populates='feedbacks')

class Complaint(Base):
    __tablename__ = 'complaints'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=True)
    makro_id = Column(String, nullable=True)
    complaint_text = Column(Text)
    status = Column(String, default='pending')
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)  # جديد: وقت حل الشكوى
    # علاقات
    route = relationship('Route', back_populates='complaints')
    user = relationship('User', back_populates='complaints')

# Enhanced User model for authentication
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    full_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)  # New field for admin privileges
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # OAuth fields
    google_id = Column(String, unique=True, nullable=True)
    google_email = Column(String, nullable=True)
    
    # علاقات
    complaints = relationship('Complaint', back_populates='user')
    sent_friendships = relationship('Friendship', foreign_keys='Friendship.user_id', back_populates='user')
    received_friendships = relationship('Friendship', foreign_keys='Friendship.friend_id', back_populates='friend')
    location_shares = relationship('LocationShare', foreign_keys='LocationShare.user_id', back_populates='user')
    received_location_shares = relationship('LocationShare', foreign_keys='LocationShare.shared_with_id', back_populates='shared_with')

# Friendship model
class Friendship(Base):
    __tablename__ = 'friendships'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(FriendshipStatus), default=FriendshipStatus.PENDING)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # علاقات
    user = relationship('User', foreign_keys=[user_id], back_populates='sent_friendships')
    friend = relationship('User', foreign_keys=[friend_id], back_populates='received_friendships')

# Location sharing model
class LocationShare(Base):
    __tablename__ = 'location_shares'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    shared_with_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Location data
    current_lat = Column(Float, nullable=False)
    current_lng = Column(Float, nullable=False)
    destination_lat = Column(Float, nullable=True)
    destination_lng = Column(Float, nullable=True)
    destination_name = Column(String, nullable=True)
    
    # Trip details
    estimated_arrival = Column(DateTime, nullable=True)
    message = Column(Text, nullable=True)
    
    # Status and timing
    status = Column(Enum(LocationSharingStatus), default=LocationSharingStatus.ACTIVE)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # علاقات
    user = relationship('User', foreign_keys=[user_id], back_populates='location_shares')
    shared_with = relationship('User', foreign_keys=[shared_with_id], back_populates='received_location_shares')

class MakroLocation(Base):
    __tablename__ = 'makro_locations'
    id = Column(Integer, primary_key=True, index=True)
    makro_id = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    geom = Column(Geometry('POINT'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class SearchLog(Base):
    __tablename__ = 'search_logs'
    id = Column(Integer, primary_key=True, index=True)
    start_lat = Column(Float, nullable=False)
    start_lng = Column(Float, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lng = Column(Float, nullable=False)
    filter_type = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class UserLocation(Base):
    __tablename__ = 'user_locations'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lat = Column(Float)
    lng = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AnalyticsData(Base):
    __tablename__ = 'analytics_data'
    id = Column(Integer, primary_key=True, index=True)
    data_type = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow) 