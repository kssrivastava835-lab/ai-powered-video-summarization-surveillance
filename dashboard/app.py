import streamlit as st
from pathlib import Path
import json


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Surveillance Dashboard",
    page_icon="🎥",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

VIDEO_PATH = BASE_DIR / "videos" / "sample.mp4"

SUMMARY_PATH = BASE_DIR / "output" / "summary.mp4"

TIMELINE_PATH = (
    BASE_DIR
    / "output"
    / "timeline"
    / "timeline.json"
)

REPORT_PATH = (
    BASE_DIR
    / "output"
    / "reports"
    / "surveillance_report.json"
)

CLIPS_FOLDER = BASE_DIR / "clips"


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):

    if not path.exists():
        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        st.error(
            f"Error loading {path.name}: {error}"
        )

        return {}


# ============================================================
# LOAD DATA
# ============================================================

report = load_json(REPORT_PATH)

timeline_data = load_json(TIMELINE_PATH)


# ============================================================
# GET EVENTS SAFELY
# ============================================================

events = []

if isinstance(timeline_data, dict):

    events = timeline_data.get(
        "events",
        []
    )

elif isinstance(timeline_data, list):

    events = timeline_data


# ============================================================
# HEADER
# ============================================================

st.title(
    "🎥 AI-Powered Video Summarization"
)

st.subheader(
    "Surveillance Analysis Dashboard"
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "Navigation"
)

page = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "Original Video",
        "Summary Video",
        "Event Timeline",
        "Event Clips",
        "Report"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header(
        "📊 System Overview"
    )

    total_events = report.get(
        "total_events",
        0
    )

    person_events = report.get(
        "person_events",
        0
    )

    vehicle_events = report.get(
        "vehicle_events",
        0
    )

    clip_count = 0

    if CLIPS_FOLDER.exists():

        clip_count = len(
            list(
                CLIPS_FOLDER.glob("*.mp4")
            )
        )

    # -----------------------------------------
    # METRICS
    # -----------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Events",
            total_events
        )

    with col2:

        st.metric(
            "Person Events",
            person_events
        )

    with col3:

        st.metric(
            "Vehicle Events",
            vehicle_events
        )

    with col4:

        st.metric(
            "Event Clips",
            clip_count
        )

    st.divider()

    st.subheader(
        "🤖 AI Processing Pipeline"
    )

    st.write(
        """
        🎥 Input Video
        ↓
        🖼️ Frame Extraction
        ↓
        🏃 Motion Detection
        ↓
        🎯 YOLO Object Detection
        ↓
        🔄 Object Tracking
        ↓
        🚨 Event Detection
        ↓
        ✂️ Event Clip Extraction
        ↓
        🎬 Summary Video
        ↓
        🕒 Timeline
        ↓
        📊 Report
        """
    )

    st.divider()

    st.subheader(
        "🚨 Detected Events"
    )

    if events:

        for event in events:

            if not isinstance(event, dict):
                continue

            event_id = event.get(
                "event_id",
                "N/A"
            )

            event_name = event.get(
                "event",
                "Unknown Event"
            )

            timestamp = event.get(
                "timestamp",
                0
            )

            event_class = event.get(
                "class",
                "Unknown"
            )

            count = event.get(
                "count",
                0
            )

            st.info(
                f"**Event {event_id}: "
                f"{event_name}** | "
                f"{timestamp:.2f}s | "
                f"{event_class} | "
                f"Count: {count}"
            )

    else:

        st.info(
            "No events found."
        )


# ============================================================
# ORIGINAL VIDEO
# ============================================================

elif page == "Original Video":

    st.header(
        "🎥 Original Surveillance Video"
    )

    if VIDEO_PATH.exists():

        st.video(
            str(VIDEO_PATH)
        )

    else:

        st.error(
            "Original video not found."
        )

        st.code(
            str(VIDEO_PATH)
        )


# ============================================================
# SUMMARY VIDEO
# ============================================================

elif page == "Summary Video":

    st.header(
        "🎬 Generated Summary Video"
    )

    if SUMMARY_PATH.exists():

        st.video(
            str(SUMMARY_PATH)
        )

        st.success(
            "Summary video loaded successfully."
        )

    else:

        st.warning(
            "Summary video not found."
        )

        st.write(
            "Run the pipeline first:"
        )

        st.code(
            "python main.py"
        )


# ============================================================
# EVENT TIMELINE
# ============================================================

elif page == "Event Timeline":

    st.header(
        "🕒 Event Timeline"
    )

    if not TIMELINE_PATH.exists():

        st.warning(
            "Timeline file not found."
        )

    else:

        total_events = 0

        if isinstance(timeline_data, dict):

            total_events = timeline_data.get(
                "total_events",
                len(events)
            )

        else:

            total_events = len(events)

        st.write(
            f"**Total Events: {total_events}**"
        )

        st.divider()

        if not events:

            st.info(
                "No events found."
            )

        else:

            for event in events:

                # -----------------------------------------
                # SAFETY CHECK
                # -----------------------------------------

                if not isinstance(event, dict):
                    continue

                event_id = event.get(
                    "event_id",
                    "N/A"
                )

                event_name = event.get(
                    "event",
                    "Unknown Event"
                )

                event_class = event.get(
                    "class",
                    "Unknown"
                )

                timestamp = event.get(
                    "timestamp",
                    0
                )

                count = event.get(
                    "count",
                    0
                )

                # -----------------------------------------
                # EVENT
                # -----------------------------------------

                st.subheader(
                    f"🚨 Event {event_id}: "
                    f"{event_name}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Timestamp",
                        f"{timestamp:.2f}s"
                    )

                with col2:

                    st.metric(
                        "Object Class",
                        event_class
                    )

                with col3:

                    st.metric(
                        "Object Count",
                        count
                    )

                st.write(
                    f"**Event:** {event_name}"
                )

                st.write(
                    f"**Timestamp:** "
                    f"{timestamp:.2f} seconds"
                )

                st.divider()


# ============================================================
# EVENT CLIPS
# ============================================================

elif page == "Event Clips":

    st.header(
        "🎬 Event Clips"
    )

    if not CLIPS_FOLDER.exists():

        st.warning(
            "Clips folder not found."
        )

    else:

        clip_paths = sorted(
            CLIPS_FOLDER.glob("*.mp4")
        )

        if not clip_paths:

            st.warning(
                "No event clips found."
            )

        else:

            st.write(
                f"**Total Clips: {len(clip_paths)}**"
            )

            st.divider()

            for index, clip_path in enumerate(
                clip_paths,
                start=1
            ):

                st.subheader(
                    f"🎥 Event Clip {index}"
                )

                st.write(
                    clip_path.stem
                )

                st.video(
                    str(clip_path)
                )

                st.divider()


# ============================================================
# REPORT
# ============================================================

elif page == "Report":

    st.header(
        "📊 Surveillance Report"
    )

    if not REPORT_PATH.exists():

        st.warning(
            "Report file not found."
        )

    else:

        total_events = report.get(
            "total_events",
            0
        )

        person_events = report.get(
            "person_events",
            0
        )

        vehicle_events = report.get(
            "vehicle_events",
            0
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Events",
                total_events
            )

        with col2:

            st.metric(
                "Person Events",
                person_events
            )

        with col3:

            st.metric(
                "Vehicle Events",
                vehicle_events
            )

        st.divider()

        st.subheader(
            "🚨 Event Details"
        )

        report_events = report.get(
            "events",
            []
        )

        if report_events:

            table_data = []

            for index, event in enumerate(
                report_events,
                start=1
            ):

                if not isinstance(event, dict):
                    continue

                table_data.append(
                    {
                        "Event ID": index,

                        "Timestamp":
                            f"{event.get('timestamp', 0):.2f}s",

                        "Event":
                            event.get(
                                "event",
                                "Unknown"
                            ),

                        "Class":
                            event.get(
                                "class",
                                "Unknown"
                            ),

                        "Count":
                            event.get(
                                "count",
                                0
                            )
                    }
                )

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No event information available."
            )

        st.divider()

        with st.expander(
            "🔍 View Raw JSON Report"
        ):

            st.json(
                report
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Powered Video Summarization for Surveillance | "
    "YOLO + Computer Vision + Object Tracking + Streamlit"
)