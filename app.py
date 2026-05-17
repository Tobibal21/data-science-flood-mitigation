import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

st.set_page_config(page_title="Flood Mitigation Analysis", page_icon="🌊")

st.title("🌊 Flood Mitigation Impact Analysis")
st.markdown("""
This app analyzes the effectiveness of drainage improvements on floodwater depth using a T-Test.
You can input your own sample data below to see how the statistical significance and charts update.
""")

st.sidebar.header("Data Input")
st.sidebar.write("Enter floodwater depths (comma-separated, in cm):")

before_input = st.sidebar.text_input("Before Improvement", "15, 18, 20, 22, 25, 21, 19")
after_input = st.sidebar.text_input("After Improvement", "7, 9, 8, 6, 10, 9, 7")

try:
    before_data = [float(x.strip()) for x in before_input.split(",")]
    after_data = [float(x.strip()) for x in after_input.split(",")]
    
    if len(before_data) < 2 or len(after_data) < 2:
        st.error("Please enter at least two data points for each category.")
    else:
        # Perform T-Test (Using independent t-test as in original notebook)
        t_stat, p_value = stats.ttest_ind(before_data, after_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Statistical Results")
            st.write(f"**T-Statistic:** `{t_stat:.4f}`")
            st.write(f"**P-Value:** `{p_value:.4f}`")
            
            st.markdown("---")
            st.write("**Conclusion based on P-Value (< 0.05):**")
            if p_value < 0.05:
                st.success("✅ Reject the null hypothesis: Drainage systems significantly reduced flooding.")
            else:
                st.warning("⚠️ Fail to reject the null hypothesis: No significant flood reduction observed.")
                
            st.markdown("---")
            st.write("**Average Flood Depth (cm):**")
            st.write(f"- Before: `{np.mean(before_data):.2f}`")
            st.write(f"- After: `{np.mean(after_data):.2f}`")
                
        with col2:
            st.subheader("Visualization")
            fig, ax = plt.subplots()
            categories = ["Before Improvement", "After Improvement"]
            # The original notebook plotted sum, but average is more intuitive for varying array lengths
            # However, I will plot the average since it makes more statistical sense
            values = [np.mean(before_data), np.mean(after_data)]
            
            ax.bar(categories, values, color=['#ff4b4b', '#1f77b4'], edgecolor='black')
            ax.set_ylabel("Average Floodwater Depth (cm)")
            ax.set_title("Impact of Drainage Improvement")
            
            # Add value labels on top of bars
            for i, v in enumerate(values):
                ax.text(i, v + 0.5, f"{v:.1f}", ha='center', fontweight='bold')
                
            st.pyplot(fig)
            
except ValueError:
    st.error("Invalid input! Please enter only numbers separated by commas.")
