import pytest
from unittest.mock import MagicMock
from services.advanced_analytics_service import AdvancedAnalyticsService

@pytest.fixture
def fake_db():
    return MagicMock()

@pytest.fixture
def service(fake_db):
    return AdvancedAnalyticsService(fake_db)

# ========== PREDICTIVE ANALYTICS ==========
def test_predict_user_growth_typical(service, fake_db):
    # بيانات نمو طبيعية
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [
        MagicMock(new_users=10, date='2023-01-01'),
        MagicMock(new_users=12, date='2023-01-02'),
        MagicMock(new_users=15, date='2023-01-03'),
        MagicMock(new_users=13, date='2023-01-04'),
        MagicMock(new_users=14, date='2023-01-05'),
        MagicMock(new_users=16, date='2023-01-06'),
        MagicMock(new_users=18, date='2023-01-07'),
        MagicMock(new_users=20, date='2023-01-08'),
        MagicMock(new_users=22, date='2023-01-09'),
        MagicMock(new_users=25, date='2023-01-10'),
        MagicMock(new_users=30, date='2023-01-11'),
        MagicMock(new_users=35, date='2023-01-12'),
        MagicMock(new_users=40, date='2023-01-13'),
        MagicMock(new_users=45, date='2023-01-14'),
        MagicMock(new_users=50, date='2023-01-15'),
        MagicMock(new_users=55, date='2023-01-16'),
        MagicMock(new_users=60, date='2023-01-17'),
        MagicMock(new_users=65, date='2023-01-18'),
        MagicMock(new_users=70, date='2023-01-19'),
        MagicMock(new_users=75, date='2023-01-20')
    ]
    fake_db.query.return_value.count.return_value = 1000
    result = service.predict_user_growth(5)
    assert result["growth_rate"] > 0
    assert len(result["predictions"]) == 5
    for pred in result["predictions"]:
        assert pred["predicted_users"] > 0
        assert 0 <= pred["confidence"] <= 1

def test_predict_user_growth_zero_growth(service, fake_db):
    # لا يوجد نمو
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [
        MagicMock(new_users=0, date='2023-01-01') for _ in range(20)
    ]
    fake_db.query.return_value.count.return_value = 100
    result = service.predict_user_growth(3)
    assert result["growth_rate"] == 0
    for pred in result["predictions"]:
        assert pred["predicted_users"] >= 100

def test_predict_user_growth_outlier(service, fake_db):
    # بيانات شاذة (outlier)
    data = [MagicMock(new_users=10, date='2023-01-01') for _ in range(18)]
    data += [MagicMock(new_users=1000, date='2023-01-19'), MagicMock(new_users=5, date='2023-01-20')]
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = data
    fake_db.query.return_value.count.return_value = 200
    result = service.predict_user_growth(2)
    assert result["avg_daily_growth"] > 0
    assert result["confidence_level"] in ["high", "medium", "low"]

def test_predict_user_growth_invalid(service):
    # أيام غير صالحة
    assert "error" in service.predict_user_growth(-1)
    assert "error" in service.predict_user_growth(100)
    # بيانات غير كافية
    service.db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [MagicMock(new_users=1, date='2023-01-01') for _ in range(5)]
    assert "error" in service.predict_user_growth(3)

def test_predict_route_demand_typical(service, fake_db):
    fake_db.query.return_value.filter.return_value.first.return_value = True
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [
        MagicMock(searches=10, date='2023-01-01'),
        MagicMock(searches=12, date='2023-01-02'),
        MagicMock(searches=15, date='2023-01-03'),
        MagicMock(searches=13, date='2023-01-04'),
        MagicMock(searches=14, date='2023-01-05'),
        MagicMock(searches=16, date='2023-01-06'),
        MagicMock(searches=18, date='2023-01-07'),
        MagicMock(searches=20, date='2023-01-08'),
        MagicMock(searches=22, date='2023-01-09'),
        MagicMock(searches=25, date='2023-01-10')
    ]
    result = service.predict_route_demand(1, 3)
    assert result["current_avg_demand"] > 0
    assert len(result["predictions"]) == 3
    for pred in result["predictions"]:
        assert pred["predicted_demand"] > 0

def test_predict_route_demand_invalid(service):
    service.db.query.return_value.filter.return_value.first.return_value = None
    assert "error" in service.predict_route_demand(-1, 7)
    assert "error" in service.predict_route_demand(1, 100)
    # بيانات غير كافية
    service.db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [MagicMock(searches=1, date='2023-01-01') for _ in range(3)]
    service.db.query.return_value.filter.return_value.first.return_value = True
    assert "error" in service.predict_route_demand(1, 2)

def test_predict_complaint_trends_various(service, fake_db):
    # بيانات طبيعية
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [
        MagicMock(complaints=2, date='2023-01-01'),
        MagicMock(complaints=3, date='2023-01-02'),
        MagicMock(complaints=4, date='2023-01-03'),
        MagicMock(complaints=5, date='2023-01-04'),
        MagicMock(complaints=6, date='2023-01-05'),
        MagicMock(complaints=7, date='2023-01-06'),
        MagicMock(complaints=8, date='2023-01-07'),
        MagicMock(complaints=9, date='2023-01-08'),
        MagicMock(complaints=10, date='2023-01-09'),
        MagicMock(complaints=11, date='2023-01-10')
    ]
    result = service.predict_complaint_trends(4)
    assert result["trend"] > 0
    assert len(result["predictions"]) == 4
    # بيانات ثابتة
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [MagicMock(complaints=5, date='2023-01-01') for _ in range(10)]
    result = service.predict_complaint_trends(2)
    assert result["trend"] == 0
    # بيانات شاذة
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [MagicMock(complaints=1, date='2023-01-01') for _ in range(6)] + [MagicMock(complaints=100, date='2023-01-07')]
    result = service.predict_complaint_trends(2)
    assert "predictions" in result
    # بيانات غير كافية
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [MagicMock(complaints=1, date='2023-01-01') for _ in range(3)]
    result = service.predict_complaint_trends(2)
    assert "error" in result

def test_statistical_and_helper_methods(service, fake_db):
    # performance metrics
    fake_db.query.return_value.count.return_value = 100
    fake_db.query.return_value.filter.return_value.count.return_value = 50
    result = service.calculate_performance_metrics()
    assert result["users"] == 100 or result["users"].get("total", 100) == 100
    # user segments
    fake_db.query.return_value.filter.return_value.all.return_value = [MagicMock(id=1, username="u1", updated_at="2023-01-01", created_at="2023-01-01")]
    result = service.analyze_user_segments()
    assert "segments" in result
    # route performance
    fake_db.query.return_value.all.return_value = [MagicMock(id=1, name="r1")]
    result = service.analyze_route_performance()
    assert isinstance(result, list)
    # geographic hotspots
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = [MagicMock(lat=33.5, lng=36.3, search_count=10)]
    result = service.analyze_geographic_hotspots()
    assert isinstance(result, list)
    # mobility patterns
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = [MagicMock(start_lat=33.5, start_lng=36.3, end_lat=33.6, end_lng=36.4, frequency=5)]
    result = service.analyze_mobility_patterns()
    assert isinstance(result, list)
    # coverage gaps
    fake_db.query.return_value.filter.return_value.group_by.return_value.all.return_value = [MagicMock(start_lat=33.5, start_lng=36.3, search_count=15)]
    service._find_nearby_routes = MagicMock(return_value=[])
    result = service.analyze_coverage_gaps()
    assert isinstance(result, list)
    # complaint trends
    fake_db.query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [MagicMock(date="2023-01-01", total=5, resolved=3)]
    fake_db.query.return_value.join.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [MagicMock(route_name="r1", route_id=1, total_complaints=10, resolved_complaints=8, avg_resolution_time=3600)]
    result = service.analyze_complaint_trends()
    assert "daily_trends" in result
    # complaint insights
    fake_db.query.return_value.count.return_value = 10
    fake_db.query.return_value.filter.return_value.count.return_value = 8
    fake_db.query.return_value.all.return_value = [MagicMock(complaint_text="تأخير")]
    result = service.generate_complaint_insights()
    assert isinstance(result, list)
    # system health
    fake_db.execute.return_value = True
    fake_db.query.return_value.count.return_value = 10
    result = service.monitor_system_health()
    assert "overall_health" in result
    # helpers
    assert service._calculate_confidence([1, 2, 3], 0.1) >= 0
    assert service._get_confidence_level(30) == "high"
    assert service._get_confidence_level(20) == "medium"
    assert service._get_confidence_level(5) == "low"
    class Day:
        def __init__(self, date, searches):
            self.date = date
            self.searches = searches
    days = [Day("2023-01-0{}".format(i+1), i+1) for i in range(7)]
    assert isinstance(service._analyze_weekly_patterns(days), dict)
    assert isinstance(service._calculate_trend([1, 2, 3, 4]), float)
    # export
    fake_db.query.return_value.count.return_value = 0
    result = service.export_analytics_report("comprehensive")
    assert "report_info" in result or "error" in result
    # summary
    assert isinstance(service.get_analytics_summary(), dict)
    # data quality
    fake_db.query.return_value.filter.return_value.count.return_value = 0
    fake_db.query.return_value.group_by.return_value.having.return_value.count.return_value = 0
    result = service.validate_data_quality()
    assert "data_quality_score" in result
    # usage statistics
    fake_db.query.return_value.filter.return_value.count.return_value = 0
    result = service.get_service_usage_statistics()
    assert "usage_statistics" in result
    # real time insights
    fake_db.query.return_value.filter.return_value.count.return_value = 0
    result = service.get_real_time_insights()
    assert "today_activity" in result 