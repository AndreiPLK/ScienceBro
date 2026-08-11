"""Adapters to optional donor systems (roadmap §7).

Every adapter must degrade gracefully: if the donor tool is absent, the adapter
reports `available() == False` and the core continues with filesystem fallbacks.
"""
