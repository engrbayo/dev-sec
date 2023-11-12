terraform {
  source = "../../../..//infrastructure/region/awssso"
}


include {
  path = find_in_parent_folders()
}
