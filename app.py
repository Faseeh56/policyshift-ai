
import streamlit as st

from src.policyshift.analyzer import analyze_policies

st.set_page_config(
    page_title="PolicyShift AI",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 PolicyShift AI")
st.caption("Evidence-backed policy change intelligence • Powered by Gemma 4")

st.markdown(
    "Compare policy versions, inspect supporting evidence, "
    "and understand how changes may affect customers."
)

with st.sidebar:
    st.header("About")
    st.write(
        "PolicyShift AI uses Google's Gemma 4 to identify "
        "meaningful changes between policy versions."
    )
    st.info(
        "Evidence verification confirms that quoted passages "
        "exist in the supplied documents. It does not guarantee "
        "the accuracy of AI interpretations."
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Previous policy")
    old_policy = st.text_area(
        "Paste the previous version",
        height=260,
        placeholder="Enter the old policy...",
    )

with col2:
    st.subheader("Updated policy")
    new_policy = st.text_area(
        "Paste the updated version",
        height=260,
        placeholder="Enter the new policy...",
    )

analyze = st.button(
    "Analyze policy changes",
    type="primary",
    use_container_width=True,
)

if analyze:
    if not old_policy.strip() or not new_policy.strip():
        st.error("Please provide both policy versions.")

    elif old_policy.strip() == new_policy.strip():
        st.success("The supplied policies are identical.")

    else:
        try:
            with st.spinner("Gemma 4 is analyzing policy changes..."):
                changes = analyze_policies(old_policy, new_policy)

            if not changes:
                st.info("No meaningful changes were identified.")

            else:
                st.divider()
                st.header("Policy Change Report")

                verified_count = sum(
                    change["evidence_verified"]
                    for change in changes
                )

                m1, m2, m3 = st.columns(3)
                m1.metric("Changes detected", len(changes))
                m2.metric("Evidence verified", verified_count)
                m3.metric(
                    "Needs review",
                    len(changes) - verified_count
                )

                if verified_count != len(changes):
                    st.warning(
                        "Some supporting quotations could not be "
                        "verified. Review these findings manually."
                    )

                for index, change in enumerate(changes, start=1):
                    with st.container(border=True):
                        st.subheader(
                            f"{index}. {change.get('topic', 'Policy change')}"
                        )

                        if change["evidence_verified"]:
                            st.success("Source quotations verified")
                        else:
                            st.warning("Source evidence needs review")

                        before, after = st.columns(2)

                        with before:
                            st.markdown("**Previous rule**")
                            st.write(change.get("old_evidence", ""))

                        with after:
                            st.markdown("**Updated rule**")
                            st.write(change.get("new_evidence", ""))

                        st.markdown("**Customer impact**")
                        st.write(change.get("customer_impact", ""))

                        st.markdown("**Recommended action**")
                        st.write(change.get("suggested_action", ""))

                st.caption(
                    "AI-generated analysis. Verify interpretations "
                    "before making business or policy decisions."
                )

        except Exception as exc:
            st.error("Policy analysis failed.")
            st.exception(exc)
