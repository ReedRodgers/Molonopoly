# Get all Simulation files
for file in `ls MoloSim*.csv`
do
  # Indicate which file we're currently processing
  echo "$file"

  # Create output file name(s)
  owned_properties=$(echo "$file" | cut -d'.' -f 1)"_owned.csv"
  unowned_properties=$(echo "$file" | cut -d'.' -f 1)"_unowned.csv"

  # Get properties
  tail -n +2 "$file" | cut -d'[' -f 2 | cut -d']' -f 1 > p1_properties.csv
  tail -n +2 "$file" | cut -d'[' -f 3 | cut -d']' -f 1 > p2_properties.csv

  # Merge together
  paste -d", " p1_properties.csv p2_properties.csv > "$owned_properties"

  # Run python audition script
  python audit_properties.py "$owned_properties" "$unowned_properties"

  # Clean up
  rm "$owned_properties"
  rm p1_properties.csv
  rm p2_properties.csv

done
