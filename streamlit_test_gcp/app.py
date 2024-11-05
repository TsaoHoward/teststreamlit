import streamlit as st
from menu import menu
import streamlit.components.v1 as components

menu()

html_content = """
<div>
    <div class="tableauPlaceholder" id="viz1730433030306" style="width: 100%; height: 100vh;">
      <noscript>
        <a href="#">
          <img alt="總儀錶板" src="https://public.tableau.com/static/images/da/dashboard_17298362302980/sheet0/1_rss.png" style="border: none" />
        </a>
      </noscript>
      <object class="tableauViz" style="width: 100%; height: 100%;">
        <param name="host_url" value="https%3A%2F%2Fpublic.tableau.com%2F" />
        <param name="embed_code_version" value="3" />
        <param name="site_root" value="" />
        <param name="name" value="dashboard_17298362302980/sheet0" />
        <param name="tabs" value="no" />
        <param name="toolbar" value="no" />
        <param name="static_image" value="https://public.tableau.com/static/images/da/dashboard_17298362302980/sheet0/1.png" />
        <param name="animate_transition" value="yes" />
        <param name="display_static_image" value="yes" />
        <param name="display_spinner" value="yes" />
        <param name="display_overlay" value="yes" />
        <param name="display_count" value="yes" />
        <param name="language" value="zh-TW" />
        <param name="filter" value="publish=yes" />
      </object>
    </div>
  </div>

  <script type='text/javascript'>
    var divElement = document.getElementById('viz1730433030306');
    var vizElement = divElement.getElementsByTagName('object')[0];
    
    // 根據螢幕寬度動態設置大小
    if (window.innerWidth > 800) {
      vizElement.style.width = '1000px';
      vizElement.style.height = '827px';
    } else if (window.innerWidth > 500) {
      vizElement.style.width = '100%';
      vizElement.style.height = '1000px';
    } else {
      vizElement.style.width = '100%';
      vizElement.style.height = '1200px';
    }
    
    // 加載 Tableau JavaScript API
    var scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
  </script>
"""
components.html(html_content, height=1000, width=1000, scrolling=True)
# st.html(html_content, height=1000, width=1000)
# components.html(html_content, height=None, width=1000)

# st.html("""
# <style>
#     iframe[width="0"] {
#         min-width: 100% !important;
#         width: 100% !important;
#         height: auto !important;
#         background-color: red !important;
#     }
# </style>
# """)

# style="position: relative; width: 100%; height: 100vh;"