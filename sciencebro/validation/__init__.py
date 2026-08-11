"""Independent validation: records live in projects/<id>/validations/*.yaml.

The scientific validator for the AInstein audit is a SEPARATE package under
projects/ainstein-audit/verifier/ and must not import upstream loss functions
(roadmap §6 rule 18, §15 independence requirement).
"""
