import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta


class BlueprintOrderAnalysis:
    def __init__(self):
        self.fraud_detector = IsolationForest(contamination=0.01)

    def process_orders(self, orders_df):
        """
        Process incoming orders for fraud detection and inventory impact

        Parameters:
        orders_df (pd.DataFrame): DataFrame with columns:
            - order_id
            - customer_id
            - products
            - total_amount
            - timestamp
        """
        # Enrich order data
        enriched_orders = self._enrich_order_data(orders_df)

        # Detect potential fraud
        fraud_scores = self._detect_fraud(enriched_orders)

        # Analyze inventory impact
        inventory_impact = self._analyze_inventory_impact(enriched_orders)

        return {
            'fraud_detection': fraud_scores,
            'inventory_impact': inventory_impact
        }

    def forecast_demand(self, historical_orders, forecast_periods=30):
        """
        Forecast demand for each product category
        """
        # Group by date and product category
        daily_demand = historical_orders.groupby(
            ['date', 'product_category'])['quantity'].sum().reset_index()

        forecasts = {}
        for category in daily_demand['product_category'].unique():
            category_demand = daily_demand[
                daily_demand['product_category'] == category
                ].set_index('date')['quantity']

            # Calculate trend
            trend = np.polyfit(range(len(category_demand)), category_demand, 1)
            forecast = np.poly1d(trend)(range(len(category_demand),
                                              len(category_demand) + forecast_periods))

            forecasts[category] = forecast.tolist()

        return forecasts

    def analyze_subscription_patterns(self, subscription_data):
        """
        Analyze subscription patterns and churn risk
        """
        # Calculate key metrics
        metrics = {
            'active_subscriptions': len(subscription_data),
            'churn_risk': self._calculate_churn_risk(subscription_data),
            'subscription_health': self._analyze_subscription_health(subscription_data)
        }

        return metrics

    def _enrich_order_data(self, orders_df):
        """Add derived features for analysis"""
        enriched = orders_df.copy()

        # Add time-based features
        enriched['hour'] = pd.to_datetime(enriched['timestamp']).dt.hour
        enriched['day_of_week'] = pd.to_datetime(enriched['timestamp']).dt.dayofweek

        # Add customer history features
        customer_history = orders_df.groupby('customer_id').agg({
            'order_id': 'count',
            'total_amount': 'mean'
        }).reset_index()

        enriched = enriched.merge(customer_history,
                                  on='customer_id',
                                  suffixes=('', '_history'))

        return enriched

    def _detect_fraud(self, orders_df):
        """Detect potentially fraudulent orders"""
        # Extract relevant features for fraud detection
        features = orders_df[[
            'total_amount',
            'hour',
            'day_of_week',
            'order_id_history',
            'total_amount_history'
        ]]

        # Fit and predict
        predictions = self.fraud_detector.fit_predict(features)

        # Return fraud scores
        return pd.Series(predictions, index=orders_df.index)

    def _analyze_inventory_impact(self, orders_df):
        """Analyze how orders affect inventory levels"""
        # Group by product and calculate demand
        product_demand = orders_df.explode('products').groupby('products').agg({
            'order_id': 'count'
        }).reset_index()

        # Calculate inventory metrics
        inventory_metrics = {
            'high_demand_products': product_demand.nlargest(5, 'order_id')['products'].tolist(),
            'total_product_demand': product_demand['order_id'].sum(),
            'demand_distribution': product_demand.set_index('products')['order_id'].to_dict()
        }

        return inventory_metrics


class InventoryOptimization:
    def __init__(self, lead_time_days=14, safety_stock_factor=1.5):
        self.lead_time_days = lead_time_days
        self.safety_stock_factor = safety_stock_factor

    def calculate_reorder_points(self, inventory_data, sales_history):
        """
        Calculate reorder points for each product
        """
        reorder_points = {}

        for product in inventory_data.index:
            # Calculate average daily demand
            daily_demand = sales_history[sales_history['product'] == product]['quantity'].mean()

            # Calculate safety stock
            demand_std = sales_history[sales_history['product'] == product]['quantity'].std()
            safety_stock = demand_std * self.safety_stock_factor * np.sqrt(self.lead_time_days)

            # Calculate reorder point
            reorder_point = (daily_demand * self.lead_time_days) + safety_stock

            reorder_points[product] = {
                'reorder_point': reorder_point,
                'safety_stock': safety_stock,
                'avg_daily_demand': daily_demand
            }

        return reorder_points

    def optimize_order_quantities(self, inventory_data, sales_history, carrying_cost_rate=0.2):
        """
        Calculate optimal order quantities using Economic Order Quantity (EOQ) formula
        """
        order_quantities = {}

        for product in inventory_data.index:
            # Get product specific data
            annual_demand = sales_history[sales_history['product'] == product]['quantity'].sum() * (
                        365 / len(sales_history))
            ordering_cost = inventory_data.loc[product, 'ordering_cost']
            unit_cost = inventory_data.loc[product, 'unit_cost']

            # Calculate EOQ (Economic Order Quantity)
            eoq = np.sqrt((2 * annual_demand * ordering_cost) / (unit_cost * carrying_cost_rate))

            order_quantities[product] = {
                'eoq': eoq,
                'annual_demand': annual_demand,
                'total_annual_cost': self._calculate_total_cost(
                    annual_demand, eoq, ordering_cost, unit_cost, carrying_cost_rate
                )
            }

        return order_quantities

    def _calculate_total_cost(self, annual_demand, order_quantity, ordering_cost,
                              unit_cost, carrying_cost_rate):
        """Calculate total annual inventory cost"""
        # Number of orders per year
        annual_orders = annual_demand / order_quantity

        # Annual ordering cost
        annual_ordering_cost = annual_orders * ordering_cost

        # Average inventory level
        avg_inventory = order_quantity / 2

        # Annual carrying cost
        annual_carrying_cost = avg_inventory * unit_cost * carrying_cost_rate

        return annual_ordering_cost + annual_carrying_cost

    def generate_inventory_report(self, inventory_data, sales_history):
        """
        Generate comprehensive inventory optimization report
        """
        reorder_points = self.calculate_reorder_points(inventory_data, sales_history)
        optimal_quantities = self.optimize_order_quantities(inventory_data, sales_history)

        report = {
            'inventory_optimization': {
                'reorder_points': reorder_points,
                'optimal_quantities': optimal_quantities
            },
            'inventory_health': self._calculate_inventory_health(inventory_data),
            'recommendations': self._generate_recommendations(
                inventory_data, reorder_points, optimal_quantities
            )
        }

        return report

    def _calculate_inventory_health(self, inventory_data):
        """Calculate inventory health metrics"""
        metrics = {
            'total_inventory_value': (
                    inventory_data['quantity_on_hand'] * inventory_data['unit_cost']
            ).sum(),
            'stock_outs': len(inventory_data[inventory_data['quantity_on_hand'] == 0]),
            'overstock_items': len(
                inventory_data[inventory_data['quantity_on_hand'] >
                               inventory_data['max_stock_level']]
            )
        }

        return metrics

    def _generate_recommendations(self, inventory_data, reorder_points, optimal_quantities):
        """Generate actionable inventory recommendations"""
        recommendations = []

        for product in inventory_data.index:
            current_stock = inventory_data.loc[product, 'quantity_on_hand']
            reorder_point = reorder_points[product]['reorder_point']
            optimal_qty = optimal_quantities[product]['eoq']

            if current_stock <= reorder_point:
                recommendations.append({
                    'product': product,
                    'action': 'REORDER',
                    'quantity': optimal_qty,
                    'urgency': 'HIGH' if current_stock == 0 else 'MEDIUM'
                })
            elif current_stock > inventory_data.loc[product, 'max_stock_level']:
                recommendations.append({
                    'product': product,
                    'action': 'REDUCE',
                    'quantity': current_stock - inventory_data.loc[product, 'max_stock_level'],
                    'urgency': 'LOW'
                })

        return recommendations
