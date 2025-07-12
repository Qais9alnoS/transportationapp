import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  RefreshControl,
  Dimensions
} from 'react-native';
import { LineChart, BarChart, PieChart } from 'react-native-chart-kit';
import { MaterialIcons, MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';

const { width } = Dimensions.get('window');

const Dashboard = ({ navigation }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [refreshing, setRefreshing] = useState(false);
  const [dashboardData, setDashboardData] = useState({});
  const [loading, setLoading] = useState(true);

  // Mock data for demonstration - replace with real API calls
  const mockData = {
    realTimeStats: {
      users: { total: 15420, active_today: 2340, new_today: 156, growth_rate: 12.5 },
      routes: { total: 45, active: 42, utilization_rate: 93.3 },
      searches: { today: 8920, week: 45670, avg_daily: 6524 },
      complaints: { today: 23, pending: 67, resolution_rate: 89.2 },
      location_sharing: { active_shares: 234, live_locations: 89 }
    },
    routeAnalytics: {
      analytics: [
        {
          route_name: "خط الجامعة - المدينة",
          performance_score: 94.5,
          search_analytics: { total_searches: 1234, active_days: 7 },
          complaint_analytics: { total_complaints: 5, resolution_rate: 100 }
        },
        {
          route_name: "خط المطار - المركز",
          performance_score: 87.2,
          search_analytics: { total_searches: 987, active_days: 6 },
          complaint_analytics: { total_complaints: 12, resolution_rate: 83.3 }
        }
      ]
    },
    userBehavior: {
      user_segments: { total_users: 15420, active_users: 8900, engagement_rate: 57.8 },
      usage_patterns: [
        { username: "أحمد محمد", activity_score: 156, searches_count: 45, user_type: "power_user" },
        { username: "فاطمة علي", activity_score: 89, searches_count: 23, user_type: "regular_user" }
      ]
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // Replace with actual API calls
      // const response = await fetch('/api/v1/dashboard/real-time-stats');
      // const data = await response.json();
      setDashboardData(mockData);
    } catch (error) {
      Alert.alert('خطأ', 'فشل في تحميل بيانات لوحة التحكم');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const renderOverviewTab = () => (
    <ScrollView style={styles.tabContent}>
      {/* Real-time Stats Cards */}
      <View style={styles.statsGrid}>
        <View style={styles.statCard}>
          <MaterialIcons name="people" size={24} color="#4CAF50" />
          <Text style={styles.statNumber}>{dashboardData.realTimeStats?.users?.total?.toLocaleString()}</Text>
          <Text style={styles.statLabel}>إجمالي المستخدمين</Text>
          <Text style={styles.statChange}>+{dashboardData.realTimeStats?.users?.growth_rate}%</Text>
        </View>

        <View style={styles.statCard}>
          <MaterialCommunityIcons name="bus" size={24} color="#2196F3" />
          <Text style={styles.statNumber}>{dashboardData.realTimeStats?.routes?.total}</Text>
          <Text style={styles.statLabel}>الخطوط النشطة</Text>
          <Text style={styles.statChange}>{dashboardData.realTimeStats?.routes?.utilization_rate}%</Text>
        </View>

        <View style={styles.statCard}>
          <MaterialIcons name="search" size={24} color="#FF9800" />
          <Text style={styles.statNumber}>{dashboardData.realTimeStats?.searches?.today?.toLocaleString()}</Text>
          <Text style={styles.statLabel}>عمليات البحث اليوم</Text>
          <Text style={styles.statChange}>+15.2%</Text>
        </View>

        <View style={styles.statCard}>
          <MaterialIcons name="report-problem" size={24} color="#F44336" />
          <Text style={styles.statNumber}>{dashboardData.realTimeStats?.complaints?.pending}</Text>
          <Text style={styles.statLabel}>الشكاوى المعلقة</Text>
          <Text style={styles.statChange}>{dashboardData.realTimeStats?.complaints?.resolution_rate}%</Text>
        </View>
      </View>

      {/* Charts Section */}
      <View style={styles.chartsSection}>
        <Text style={styles.sectionTitle}>تحليل النشاط الأسبوعي</Text>
        <LineChart
          data={{
            labels: ['أحد', 'اثنين', 'ثلاثاء', 'أربعاء', 'خميس', 'جمعة', 'سبت'],
            datasets: [{
              data: [6500, 7200, 6800, 7500, 8200, 7800, 7000]
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
            style: {
              borderRadius: 16
            }
          }}
          bezier
          style={styles.chart}
        />
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        <Text style={styles.sectionTitle}>إجراءات سريعة</Text>
        <View style={styles.actionButtons}>
          <TouchableOpacity style={styles.actionButton} onPress={() => navigation.navigate('Complaints')}>
            <MaterialIcons name="report-problem" size={24} color="#F44336" />
            <Text style={styles.actionText}>إدارة الشكاوى</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton} onPress={() => navigation.navigate('Routes')}>
            <MaterialCommunityIcons name="bus" size={24} color="#2196F3" />
            <Text style={styles.actionText}>إدارة الخطوط</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton} onPress={() => navigation.navigate('Users')}>
            <MaterialIcons name="people" size={24} color="#4CAF50" />
            <Text style={styles.actionText}>إدارة المستخدمين</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton} onPress={() => navigation.navigate('Analytics')}>
            <FontAwesome5 name="chart-line" size={24} color="#FF9800" />
            <Text style={styles.actionText}>تحليلات متقدمة</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );

  const renderAnalyticsTab = () => (
    <ScrollView style={styles.tabContent}>
      {/* Route Performance */}
      <View style={styles.analyticsSection}>
        <Text style={styles.sectionTitle}>أداء الخطوط</Text>
        {dashboardData.routeAnalytics?.analytics?.map((route, index) => (
          <View key={index} style={styles.routeCard}>
            <View style={styles.routeHeader}>
              <Text style={styles.routeName}>{route.route_name}</Text>
              <View style={[styles.scoreBadge, { backgroundColor: route.performance_score > 90 ? '#4CAF50' : route.performance_score > 70 ? '#FF9800' : '#F44336' }]}>
                <Text style={styles.scoreText}>{route.performance_score}%</Text>
              </View>
            </View>
            <View style={styles.routeStats}>
              <View style={styles.routeStat}>
                <Text style={styles.routeStatLabel}>عمليات البحث</Text>
                <Text style={styles.routeStatValue}>{route.search_analytics.total_searches}</Text>
              </View>
              <View style={styles.routeStat}>
                <Text style={styles.routeStatLabel}>معدل حل الشكاوى</Text>
                <Text style={styles.routeStatValue}>{route.complaint_analytics.resolution_rate}%</Text>
              </View>
            </View>
          </View>
        ))}
      </View>

      {/* User Behavior Chart */}
      <View style={styles.analyticsSection}>
        <Text style={styles.sectionTitle}>أنماط استخدام المستخدمين</Text>
        <BarChart
          data={{
            labels: ['مستخدمين نشطين', 'مستخدمين جدد', 'مستخدمين غير نشطين'],
            datasets: [{
              data: [
                dashboardData.userBehavior?.user_segments?.active_users || 0,
                dashboardData.userBehavior?.user_segments?.total_users - dashboardData.userBehavior?.user_segments?.active_users || 0,
                1000
              ]
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
            style: {
              borderRadius: 16
            }
          }}
          style={styles.chart}
        />
      </View>
    </ScrollView>
  );

  const renderReportsTab = () => (
    <ScrollView style={styles.tabContent}>
      <View style={styles.reportsSection}>
        <Text style={styles.sectionTitle}>التقارير المتاحة</Text>
        
        <TouchableOpacity style={styles.reportCard}>
          <MaterialIcons name="assessment" size={24} color="#2196F3" />
          <View style={styles.reportContent}>
            <Text style={styles.reportTitle}>تقرير الأداء الشهري</Text>
            <Text style={styles.reportDescription}>تحليل شامل لأداء جميع الخطوط والمستخدمين</Text>
          </View>
          <MaterialIcons name="arrow-forward-ios" size={20} color="#666" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.reportCard}>
          <MaterialIcons name="trending-up" size={24} color="#4CAF50" />
          <View style={styles.reportContent}>
            <Text style={styles.reportTitle}>تقرير النمو والتنبؤات</Text>
            <Text style={styles.reportDescription}>تحليل اتجاهات النمو والتوقعات المستقبلية</Text>
          </View>
          <MaterialIcons name="arrow-forward-ios" size={20} color="#666" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.reportCard}>
          <MaterialIcons name="location-on" size={24} color="#FF9800" />
          <View style={styles.reportContent}>
            <Text style={styles.reportTitle}>تقرير التغطية الجغرافية</Text>
            <Text style={styles.reportDescription}>تحليل التغطية والمناطق المطلوبة</Text>
          </View>
          <MaterialIcons name="arrow-forward-ios" size={20} color="#666" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.reportCard}>
          <MaterialIcons name="feedback" size={24} color="#F44336" />
          <View style={styles.reportContent}>
            <Text style={styles.reportTitle}>تقرير الشكاوى والرضا</Text>
            <Text style={styles.reportDescription}>تحليل الشكاوى ومعدلات الرضا</Text>
          </View>
          <MaterialIcons name="arrow-forward-ios" size={20} color="#666" />
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

  const renderSettingsTab = () => (
    <ScrollView style={styles.tabContent}>
      <View style={styles.settingsSection}>
        <Text style={styles.sectionTitle}>إعدادات لوحة التحكم</Text>
        
        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>تحديث تلقائي للبيانات</Text>
          <TouchableOpacity style={styles.toggleButton}>
            <Text style={styles.toggleText}>مفعل</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>إشعارات فورية</Text>
          <TouchableOpacity style={styles.toggleButton}>
            <Text style={styles.toggleText}>مفعل</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>تصدير التقارير</Text>
          <TouchableOpacity style={styles.toggleButton}>
            <Text style={styles.toggleText}>PDF</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity style={styles.exportButton}>
          <MaterialIcons name="file-download" size={20} color="#fff" />
          <Text style={styles.exportButtonText}>تصدير جميع البيانات</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>لوحة التحكم الحكومية</Text>
        <TouchableOpacity onPress={onRefresh} style={styles.refreshButton}>
          <MaterialIcons name="refresh" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Tab Navigation */}
      <View style={styles.tabNavigation}>
        <TouchableOpacity 
          style={[styles.tabButton, activeTab === 'overview' && styles.activeTabButton]}
          onPress={() => setActiveTab('overview')}
        >
          <MaterialIcons name="dashboard" size={20} color={activeTab === 'overview' ? '#2196F3' : '#666'} />
          <Text style={[styles.tabText, activeTab === 'overview' && styles.activeTabText]}>نظرة عامة</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.tabButton, activeTab === 'analytics' && styles.activeTabButton]}
          onPress={() => setActiveTab('analytics')}
        >
          <MaterialIcons name="analytics" size={20} color={activeTab === 'analytics' ? '#2196F3' : '#666'} />
          <Text style={[styles.tabText, activeTab === 'analytics' && styles.activeTabText]}>تحليلات</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.tabButton, activeTab === 'reports' && styles.activeTabButton]}
          onPress={() => setActiveTab('reports')}
        >
          <MaterialIcons name="assessment" size={20} color={activeTab === 'reports' ? '#2196F3' : '#666'} />
          <Text style={[styles.tabText, activeTab === 'reports' && styles.activeTabText]}>تقارير</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.tabButton, activeTab === 'settings' && styles.activeTabButton]}
          onPress={() => setActiveTab('settings')}
        >
          <MaterialIcons name="settings" size={20} color={activeTab === 'settings' ? '#2196F3' : '#666'} />
          <Text style={[styles.tabText, activeTab === 'settings' && styles.activeTabText]}>إعدادات</Text>
        </TouchableOpacity>
      </View>

      {/* Tab Content */}
      <ScrollView 
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {activeTab === 'overview' && renderOverviewTab()}
        {activeTab === 'analytics' && renderAnalyticsTab()}
        {activeTab === 'reports' && renderReportsTab()}
        {activeTab === 'settings' && renderSettingsTab()}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#2196F3',
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  refreshButton: {
    padding: 8,
  },
  tabNavigation: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    paddingHorizontal: 10,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  tabButton: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 10,
    borderRadius: 8,
  },
  activeTabButton: {
    backgroundColor: '#e3f2fd',
  },
  tabText: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  activeTabText: {
    color: '#2196F3',
    fontWeight: 'bold',
  },
  content: {
    flex: 1,
  },
  tabContent: {
    padding: 20,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  statCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    width: '48%',
    marginBottom: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  statChange: {
    fontSize: 10,
    color: '#4CAF50',
    marginTop: 4,
    fontWeight: 'bold',
  },
  chartsSection: {
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  quickActions: {
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
  actionButtons: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionButton: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 16,
    width: '48%',
    marginBottom: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  actionText: {
    fontSize: 12,
    color: '#333',
    marginTop: 8,
    textAlign: 'center',
  },
  analyticsSection: {
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
  routeCard: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  routeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  routeName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  scoreBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  scoreText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  routeStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  routeStat: {
    alignItems: 'center',
  },
  routeStatLabel: {
    fontSize: 12,
    color: '#666',
  },
  routeStatValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  reportsSection: {
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
  reportCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  reportContent: {
    flex: 1,
    marginLeft: 16,
  },
  reportTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  reportDescription: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  settingsSection: {
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
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  settingLabel: {
    fontSize: 16,
    color: '#333',
  },
  toggleButton: {
    backgroundColor: '#2196F3',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 16,
  },
  toggleText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  exportButton: {
    backgroundColor: '#4CAF50',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 8,
    marginTop: 20,
  },
  exportButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default Dashboard; 