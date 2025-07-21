import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Dimensions,
  ActivityIndicator
} from 'react-native';
import { LineChart, BarChart, PieChart } from 'react-native-chart-kit';
import { MaterialIcons, MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';

const { width } = Dimensions.get('window');

const AdvancedAnalytics = ({ navigation }) => {
  const [activeSection, setActiveSection] = useState('predictive');
  const [loading, setLoading] = useState(false);
  const [analyticsData, setAnalyticsData] = useState({});

  // Mock advanced analytics data
  const mockAdvancedData = {
    predictive: {
      growth_analytics: {
        current_users: 15420,
        growth_rate: 12.5,
        avg_daily_growth: 156,
        historical_data: [
          { date: '2024-01-01', new_users: 120 },
          { date: '2024-01-02', new_users: 145 },
          { date: '2024-01-03', new_users: 167 },
          { date: '2024-01-04', new_users: 189 },
          { date: '2024-01-05', new_users: 201 },
          { date: '2024-01-06', new_users: 234 },
          { date: '2024-01-07', new_users: 256 }
        ]
      },
      predictions: {
        forecast_period: 7,
        predicted_growth: [
          { date: '2024-01-08', predicted_users: 15676, growth_factor: 1.125 },
          { date: '2024-01-09', predicted_users: 15832, growth_factor: 1.126 },
          { date: '2024-01-10', predicted_users: 15988, growth_factor: 1.127 },
          { date: '2024-01-11', predicted_users: 16144, growth_factor: 1.128 },
          { date: '2024-01-12', predicted_users: 16300, growth_factor: 1.129 },
          { date: '2024-01-13', predicted_users: 16456, growth_factor: 1.130 },
          { date: '2024-01-14', predicted_users: 16612, growth_factor: 1.131 }
        ],
        confidence_level: "high"
      },
      seasonal_patterns: {
        peak_hours: [
          { hour: 8, count: 2340 },
          { hour: 17, count: 1890 },
          { hour: 12, count: 1560 }
        ],
        usage_trend: [
          { date: '2024-01-01', searches: 6500 },
          { date: '2024-01-02', searches: 7200 },
          { date: '2024-01-03', searches: 6800 },
          { date: '2024-01-04', searches: 7500 },
          { date: '2024-01-05', searches: 8200 },
          { date: '2024-01-06', searches: 7800 },
          { date: '2024-01-07', searches: 7000 }
        ]
      }
    },
    geographic: {
      hotspots: [
        { lat: 24.7136, lng: 46.6753, intensity: 234, level: "high" },
        { lat: 24.7236, lng: 46.6853, intensity: 189, level: "high" },
        { lat: 24.7336, lng: 46.6953, intensity: 156, level: "medium" },
        { lat: 24.7436, lng: 46.7053, intensity: 123, level: "medium" },
        { lat: 24.7536, lng: 46.7153, intensity: 98, level: "low" }
      ],
      coverage: [
        { route_name: "خط الجامعة - المدينة", coverage_score: 95.2 },
        { route_name: "خط المطار - المركز", coverage_score: 87.8 },
        { route_name: "خط الشمال - الجنوب", coverage_score: 92.1 },
        { route_name: "خط الشرق - الغرب", coverage_score: 78.9 }
      ],
      mobility: [
        {
          start: { lat: 24.7136, lng: 46.6753 },
          end: { lat: 24.7236, lng: 46.6853 },
          frequency: 234,
          popularity: "high"
        },
        {
          start: { lat: 24.7236, lng: 46.6853 },
          end: { lat: 24.7336, lng: 46.6953 },
          frequency: 189,
          popularity: "high"
        }
      ]
    },
    complaints: {
      overview: {
        total_complaints: 234,
        resolved_complaints: 189,
        resolution_rate: 80.8,
        avg_response_time_hours: 4.2
      },
      trends: [
        { date: '2024-01-01', total: 12, resolved: 10, pending: 2 },
        { date: '2024-01-02', total: 15, resolved: 12, pending: 3 },
        { date: '2024-01-03', total: 18, resolved: 15, pending: 3 },
        { date: '2024-01-04', total: 14, resolved: 11, pending: 3 },
        { date: '2024-01-05', total: 16, resolved: 13, pending: 3 },
        { date: '2024-01-06', total: 19, resolved: 16, pending: 3 },
        { date: '2024-01-07', total: 13, resolved: 10, pending: 3 }
      ],
      categories: {
        delays: 45,
        crowding: 38,
        driver: 23,
        vehicle: 19,
        pricing: 12,
        service: 8
      }
    },
    system: {
      overall_health: "excellent",
      performance_metrics: {
        database: { status: "healthy", response_time_ms: 15 },
        api: { avg_response_time_ms: 120, error_rate: 0.02, uptime_percentage: 99.8 },
        storage: { database_size_mb: 45.2, log_size_mb: 12.8, backup_status: "up_to_date" }
      },
      error_analysis: {
        recent_errors: 0,
        error_trend: "decreasing",
        critical_issues: 0
      }
    }
  };

  useEffect(() => {
    loadAdvancedAnalytics();
  }, []);

  const loadAdvancedAnalytics = async () => {
    setLoading(true);
    try {
      // Replace with actual API calls
      // const response = await fetch('/api/v1/dashboard/predictive-insights');
      // const data = await response.json();
      setAnalyticsData(mockAdvancedData);
    } catch (error) {
      Alert.alert('خطأ', 'فشل في تحميل البيانات التحليلية المتقدمة');
    } finally {
      setLoading(false);
    }
  };

  const renderPredictiveSection = () => (
    <ScrollView style={styles.sectionContent}>
      {/* Growth Prediction Chart */}
      <View style={styles.chartCard}>
        <Text style={styles.chartTitle}>توقعات النمو المستقبلي</Text>
        <LineChart
          data={{
            labels: ['اليوم', '+1', '+2', '+3', '+4', '+5', '+6'],
            datasets: [{
              data: analyticsData.predictive?.predictions?.predicted_growth?.map(p => p.predicted_users / 1000) || []
            }]
          }}
          width={width - 40}
          height={220}
          chartConfig={{
            backgroundColor: '#ffffff',
            backgroundGradientFrom: '#ffffff',
            backgroundGradientTo: '#ffffff',
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(76, 175, 80, ${opacity})`,
            style: { borderRadius: 16 }
          }}
          bezier
          style={styles.chart}
        />
        <View style={styles.chartLegend}>
          <Text style={styles.legendText}>مستوى الثقة: {analyticsData.predictive?.predictions?.confidence_level}</Text>
        </View>
      </View>

      {/* Peak Hours Analysis */}
      <View style={styles.chartCard}>
        <Text style={styles.chartTitle}>أوقات الذروة الأسبوعية</Text>
        <BarChart
          data={{
            labels: ['8 ص', '12 م', '5 م', '8 م', '10 م'],
            datasets: [{
              data: analyticsData.predictive?.seasonal_patterns?.peak_hours?.map(h => h.count / 100) || []
            }]
          }}
          width={width - 40}
          height={220}
          chartConfig={{
            backgroundColor: '#ffffff',
            backgroundGradientFrom: '#ffffff',
            backgroundGradientTo: '#ffffff',
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(255, 152, 0, ${opacity})`,
            style: { borderRadius: 16 }
          }}
          style={styles.chart}
        />
      </View>

      {/* Growth Insights */}
      <View style={styles.insightsCard}>
        <Text style={styles.insightsTitle}>رؤى النمو</Text>
        <View style={styles.insightItem}>
          <MaterialIcons name="trending-up" size={20} color="#4CAF50" />
          <Text style={styles.insightText}>
            معدل النمو الحالي: {analyticsData.predictive?.growth_analytics?.growth_rate}%
          </Text>
        </View>
        <View style={styles.insightItem}>
          <MaterialIcons name="people" size={20} color="#2196F3" />
          <Text style={styles.insightText}>
            متوسط النمو اليومي: {analyticsData.predictive?.growth_analytics?.avg_daily_growth} مستخدم
          </Text>
        </View>
        <View style={styles.insightItem}>
          <MaterialIcons name="schedule" size={20} color="#FF9800" />
          <Text style={styles.insightText}>
            أوقات الذروة: 8 صباحاً، 5 مساءً، 8 مساءً
          </Text>
        </View>
      </View>
    </ScrollView>
  );

  const renderGeographicSection = () => (
    <ScrollView style={styles.sectionContent}>
      {/* Hotspots Map */}
      <View style={styles.mapCard}>
        <Text style={styles.mapTitle}>النقاط الساخنة الجغرافية</Text>
        <View style={styles.mapContainer}>
          <View style={styles.mapPlaceholder}>
            <MaterialCommunityIcons name="map" size={48} color="#2196F3" />
            <Text style={styles.mapPlaceholderText}>خريطة تفاعلية للنقاط الساخنة</Text>
          </View>
        </View>
        <View style={styles.hotspotsList}>
          {analyticsData.geographic?.hotspots?.map((hotspot, index) => (
            <View key={index} style={styles.hotspotItem}>
              <View style={[styles.hotspotIndicator, { backgroundColor: hotspot.level === 'high' ? '#F44336' : hotspot.level === 'medium' ? '#FF9800' : '#4CAF50' }]} />
              <View style={styles.hotspotInfo}>
                <Text style={styles.hotspotLocation}>
                  {hotspot.lat.toFixed(4)}, {hotspot.lng.toFixed(4)}
                </Text>
                <Text style={styles.hotspotIntensity}>
                  كثافة: {hotspot.intensity} عملية بحث
                </Text>
              </View>
            </View>
          ))}
        </View>
      </View>

      {/* Coverage Analysis */}
      <View style={styles.chartCard}>
        <Text style={styles.chartTitle}>تحليل التغطية الجغرافية</Text>
        <BarChart
          data={{
            labels: ['جامعة', 'مطار', 'شمال', 'شرق'],
            datasets: [{
              data: analyticsData.geographic?.coverage?.map(c => c.coverage_score) || []
            }]
          }}
          width={width - 40}
          height={220}
          chartConfig={{
            backgroundColor: '#ffffff',
            backgroundGradientFrom: '#ffffff',
            backgroundGradientTo: '#ffffff',
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(33, 150, 243, ${opacity})`,
            style: { borderRadius: 16 }
          }}
          style={styles.chart}
        />
      </View>

      {/* Mobility Patterns */}
      <View style={styles.mobilityCard}>
        <Text style={styles.mobilityTitle}>أنماط الحركة الشائعة</Text>
        {analyticsData.geographic?.mobility?.map((pattern, index) => (
          <View key={index} style={styles.mobilityItem}>
            <View style={styles.mobilityRoute}>
              <View style={styles.routePoint}>
                <Text style={styles.pointLabel}>من</Text>
                <Text style={styles.pointCoords}>
                  {pattern.start.lat.toFixed(4)}, {pattern.start.lng.toFixed(4)}
                </Text>
              </View>
              <MaterialIcons name="arrow-forward" size={20} color="#666" />
              <View style={styles.routePoint}>
                <Text style={styles.pointLabel}>إلى</Text>
                <Text style={styles.pointCoords}>
                  {pattern.end.lat.toFixed(4)}, {pattern.end.lng.toFixed(4)}
                </Text>
              </View>
            </View>
            <View style={styles.mobilityStats}>
              <Text style={styles.frequencyText}>
                التكرار: {pattern.frequency} مرة
              </Text>
              <View style={[styles.popularityBadge, { backgroundColor: pattern.popularity === 'high' ? '#4CAF50' : '#FF9800' }]}>
                <Text style={styles.popularityText}>
                  {pattern.popularity === 'high' ? 'عالية' : 'متوسطة'}
                </Text>
              </View>
            </View>
          </View>
        ))}
      </View>
    </ScrollView>
  );

  const renderComplaintsSection = () => (
    <ScrollView style={styles.sectionContent}>
      {/* Complaints Overview */}
      <View style={styles.overviewCard}>
        <Text style={styles.overviewTitle}>نظرة عامة على الشكاوى</Text>
        <View style={styles.overviewStats}>
          <View style={styles.overviewStat}>
            <Text style={styles.overviewNumber}>{analyticsData.complaints?.overview?.total_complaints}</Text>
            <Text style={styles.overviewLabel}>إجمالي الشكاوى</Text>
          </View>
          <View style={styles.overviewStat}>
            <Text style={styles.overviewNumber}>{analyticsData.complaints?.overview?.resolved_complaints}</Text>
            <Text style={styles.overviewLabel}>تم الحل</Text>
          </View>
          <View style={styles.overviewStat}>
            <Text style={styles.overviewNumber}>{analyticsData.complaints?.overview?.resolution_rate}%</Text>
            <Text style={styles.overviewLabel}>معدل الحل</Text>
          </View>
          <View style={styles.overviewStat}>
            <Text style={styles.overviewNumber}>{analyticsData.complaints?.overview?.avg_response_time_hours}h</Text>
            <Text style={styles.overviewLabel}>متوسط الاستجابة</Text>
          </View>
        </View>
      </View>

      {/* Complaints Trends */}
      <View style={styles.chartCard}>
        <Text style={styles.chartTitle}>اتجاهات الشكاوى الأسبوعية</Text>
        <LineChart
          data={{
            labels: ['أحد', 'اثنين', 'ثلاثاء', 'أربعاء', 'خميس', 'جمعة', 'سبت'],
            datasets: [
              {
                data: analyticsData.complaints?.trends?.map(t => t.total) || [],
                color: (opacity = 1) => `rgba(244, 67, 54, ${opacity})`,
                strokeWidth: 2
              },
              {
                data: analyticsData.complaints?.trends?.map(t => t.resolved) || [],
                color: (opacity = 1) => `rgba(76, 175, 80, ${opacity})`,
                strokeWidth: 2
              }
            ]
          }}
          width={width - 40}
          height={220}
          chartConfig={{
            backgroundColor: '#ffffff',
            backgroundGradientFrom: '#ffffff',
            backgroundGradientTo: '#ffffff',
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
            style: { borderRadius: 16 }
          }}
          bezier
          style={styles.chart}
        />
        <View style={styles.chartLegend}>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: '#F44336' }]} />
            <Text style={styles.legendText}>إجمالي الشكاوى</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: '#4CAF50' }]} />
            <Text style={styles.legendText}>تم الحل</Text>
          </View>
        </View>
      </View>

      {/* Complaint Categories */}
      <View style={styles.chartCard}>
        <Text style={styles.chartTitle}>تصنيف الشكاوى</Text>
        <PieChart
          data={[
            {
              name: 'تأخير',
              population: analyticsData.complaints?.categories?.delays || 0,
              color: '#F44336',
              legendFontColor: '#7F7F7F',
              legendFontSize: 12
            },
            {
              name: 'ازدحام',
              population: analyticsData.complaints?.categories?.crowding || 0,
              color: '#FF9800',
              legendFontColor: '#7F7F7F',
              legendFontSize: 12
            },
            {
              name: 'سائق',
              population: analyticsData.complaints?.categories?.driver || 0,
              color: '#2196F3',
              legendFontColor: '#7F7F7F',
              legendFontSize: 12
            },
            {
              name: 'مركبة',
              population: analyticsData.complaints?.categories?.vehicle || 0,
              color: '#9C27B0',
              legendFontColor: '#7F7F7F',
              legendFontSize: 12
            },
            {
              name: 'سعر',
              population: analyticsData.complaints?.categories?.pricing || 0,
              color: '#607D8B',
              legendFontColor: '#7F7F7F',
              legendFontSize: 12
            },
            {
              name: 'خدمة',
              population: analyticsData.complaints?.categories?.service || 0,
              color: '#795548',
              legendFontColor: '#7F7F7F',
              legendFontSize: 12
            }
          ]}
          width={width - 40}
          height={220}
          chartConfig={{
            color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
          }}
          accessor="population"
          backgroundColor="transparent"
          paddingLeft="15"
          style={styles.chart}
        />
      </View>
    </ScrollView>
  );

  const renderSystemSection = () => (
    <ScrollView style={styles.sectionContent}>
      {/* System Health Overview */}
      <View style={styles.healthCard}>
        <View style={styles.healthHeader}>
          <Text style={styles.healthTitle}>صحة النظام</Text>
          <View style={[styles.healthStatus, { backgroundColor: analyticsData.system?.overall_health === 'excellent' ? '#4CAF50' : '#F44336' }]}>
            <Text style={styles.healthStatusText}>
              {analyticsData.system?.overall_health === 'excellent' ? 'ممتازة' : 'ضعيفة'}
            </Text>
          </View>
        </View>
        
        <View style={styles.healthMetrics}>
          <View style={styles.healthMetric}>
            <MaterialIcons name="storage" size={24} color="#2196F3" />
            <View style={styles.metricInfo}>
              <Text style={styles.metricLabel}>قاعدة البيانات</Text>
              <Text style={styles.metricValue}>
                {analyticsData.system?.performance_metrics?.database?.status === 'healthy' ? 'سليمة' : 'مشكلة'}
              </Text>
              <Text style={styles.metricDetail}>
                {analyticsData.system?.performance_metrics?.database?.response_time_ms}ms
              </Text>
            </View>
          </View>

          <View style={styles.healthMetric}>
            <MaterialIcons name="api" size={24} color="#4CAF50" />
            <View style={styles.metricInfo}>
              <Text style={styles.metricLabel}>واجهة البرمجة</Text>
              <Text style={styles.metricValue}>
                {analyticsData.system?.performance_metrics?.api?.avg_response_time_ms}ms
              </Text>
              <Text style={styles.metricDetail}>
                {analyticsData.system?.performance_metrics?.api?.uptime_percentage}% متاحة
              </Text>
            </View>
          </View>

          <View style={styles.healthMetric}>
            <MaterialIcons name="cloud" size={24} color="#FF9800" />
            <View style={styles.metricInfo}>
              <Text style={styles.metricLabel}>التخزين</Text>
              <Text style={styles.metricValue}>
                {analyticsData.system?.performance_metrics?.storage?.database_size_mb}MB
              </Text>
              <Text style={styles.metricDetail}>
                {analyticsData.system?.performance_metrics?.storage?.backup_status === 'up_to_date' ? 'نسخة احتياطية محدثة' : 'نسخة احتياطية قديمة'}
              </Text>
            </View>
          </View>
        </View>
      </View>

      {/* Error Analysis */}
      <View style={styles.errorCard}>
        <Text style={styles.errorTitle}>تحليل الأخطاء</Text>
        <View style={styles.errorStats}>
          <View style={styles.errorStat}>
            <Text style={styles.errorNumber}>{analyticsData.system?.error_analysis?.recent_errors}</Text>
            <Text style={styles.errorLabel}>أخطاء حديثة</Text>
          </View>
          <View style={styles.errorStat}>
            <Text style={styles.errorNumber}>{analyticsData.system?.error_analysis?.critical_issues}</Text>
            <Text style={styles.errorLabel}>مشاكل حرجة</Text>
          </View>
          <View style={styles.errorStat}>
            <Text style={styles.errorTrend}>
              {analyticsData.system?.error_analysis?.error_trend === 'decreasing' ? 'تناقص' : 'تزايد'}
            </Text>
            <Text style={styles.errorLabel}>اتجاه الأخطاء</Text>
          </View>
        </View>
      </View>

      {/* Performance Recommendations */}
      <View style={styles.recommendationsCard}>
        <Text style={styles.recommendationsTitle}>توصيات الأداء</Text>
        <View style={styles.recommendationItem}>
          <MaterialIcons name="lightbulb" size={20} color="#FF9800" />
          <Text style={styles.recommendationText}>
            النظام يعمل بكفاءة عالية - لا توجد توصيات عاجلة
          </Text>
        </View>
        <View style={styles.recommendationItem}>
          <MaterialIcons name="schedule" size={20} color="#4CAF50" />
          <Text style={styles.recommendationText}>
            النسخ الاحتياطية تعمل بشكل منتظم
          </Text>
        </View>
        <View style={styles.recommendationItem}>
          <MaterialIcons name="speed" size={20} color="#2196F3" />
          <Text style={styles.recommendationText}>
            وقت الاستجابة ضمن النطاق المثالي
          </Text>
        </View>
      </View>
    </ScrollView>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
        <Text style={styles.loadingText}>جاري تحميل التحليلات المتقدمة...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <MaterialIcons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>التحليلات المتقدمة</Text>
        <View style={styles.headerSpacer} />
      </View>

      {/* Section Navigation */}
      <View style={styles.sectionNavigation}>
        <TouchableOpacity 
          style={[styles.sectionButton, activeSection === 'predictive' && styles.activeSectionButton]}
          onPress={() => setActiveSection('predictive')}
        >
          <MaterialIcons name="trending-up" size={20} color={activeSection === 'predictive' ? '#2196F3' : '#666'} />
          <Text style={[styles.sectionText, activeSection === 'predictive' && styles.activeSectionText]}>تنبؤات</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.sectionButton, activeSection === 'geographic' && styles.activeSectionButton]}
          onPress={() => setActiveSection('geographic')}
        >
          <MaterialCommunityIcons name="map" size={20} color={activeSection === 'geographic' ? '#2196F3' : '#666'} />
          <Text style={[styles.sectionText, activeSection === 'geographic' && styles.activeSectionText]}>جغرافية</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.sectionButton, activeSection === 'complaints' && styles.activeSectionButton]}
          onPress={() => setActiveSection('complaints')}
        >
          <MaterialIcons name="report-problem" size={20} color={activeSection === 'complaints' ? '#2196F3' : '#666'} />
          <Text style={[styles.sectionText, activeSection === 'complaints' && styles.activeSectionText]}>شكاوى</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.sectionButton, activeSection === 'system' && styles.activeSectionButton]}
          onPress={() => setActiveSection('system')}
        >
          <MaterialIcons name="computer" size={20} color={activeSection === 'system' ? '#2196F3' : '#666'} />
          <Text style={[styles.sectionText, activeSection === 'system' && styles.activeSectionText]}>النظام</Text>
        </TouchableOpacity>
      </View>

      {/* Section Content */}
      {activeSection === 'predictive' && renderPredictiveSection()}
      {activeSection === 'geographic' && renderGeographicSection()}
      {activeSection === 'complaints' && renderComplaintsSection()}
      {activeSection === 'system' && renderSystemSection()}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  header: {
    backgroundColor: '#2196F3',
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    flexDirection: 'row',
    alignItems: 'center',
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    flex: 1,
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
  },
  headerSpacer: {
    width: 40,
  },
  sectionNavigation: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    paddingHorizontal: 10,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  sectionButton: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 10,
    borderRadius: 8,
  },
  activeSectionButton: {
    backgroundColor: '#e3f2fd',
  },
  sectionText: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  activeSectionText: {
    color: '#2196F3',
    fontWeight: 'bold',
  },
  sectionContent: {
    flex: 1,
    padding: 20,
  },
  chartCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  chartTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  chartLegend: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: 8,
  },
  legendColor: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 4,
  },
  legendText: {
    fontSize: 12,
    color: '#666',
  },
  insightsCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  insightsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  insightItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  insightText: {
    fontSize: 14,
    color: '#333',
    marginLeft: 12,
  },
  mapCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  mapTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  mapContainer: {
    height: 200,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    marginBottom: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  mapPlaceholder: {
    alignItems: 'center',
  },
  mapPlaceholderText: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
  },
  hotspotsList: {
    marginTop: 16,
  },
  hotspotItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  hotspotIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 12,
  },
  hotspotInfo: {
    flex: 1,
  },
  hotspotLocation: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  hotspotIntensity: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  mobilityCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  mobilityTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  mobilityItem: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
  },
  mobilityRoute: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  routePoint: {
    flex: 1,
  },
  pointLabel: {
    fontSize: 12,
    color: '#666',
  },
  pointCoords: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  mobilityStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  frequencyText: {
    fontSize: 14,
    color: '#333',
  },
  popularityBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  popularityText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  overviewCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  overviewTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  overviewStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  overviewStat: {
    alignItems: 'center',
    flex: 1,
  },
  overviewNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  overviewLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  errorCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  errorTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  errorStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  errorStat: {
    alignItems: 'center',
    flex: 1,
  },
  errorNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#F44336',
  },
  errorTrend: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  errorLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  healthCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  healthHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  healthTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  healthStatus: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  healthStatusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  healthMetrics: {
    marginTop: 16,
  },
  healthMetric: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  metricInfo: {
    flex: 1,
    marginLeft: 12,
  },
  metricLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  metricValue: {
    fontSize: 16,
    color: '#2196F3',
    fontWeight: 'bold',
  },
  metricDetail: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  recommendationsCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  recommendationsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  recommendationItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  recommendationText: {
    fontSize: 14,
    color: '#333',
    marginLeft: 12,
    flex: 1,
  },
});

export default AdvancedAnalytics; 