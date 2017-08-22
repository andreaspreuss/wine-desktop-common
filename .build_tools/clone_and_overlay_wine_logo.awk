BEGIN{
	svg_tag_open_regexp="<svg($| )"
	svg_tag_close_regexp="</svg>"
	defs_tag_close_regexp="</defs>"
	defs_tag_open_regexp="<defs($| )"
	defs_tag_close_regexp="</defs>"
	group_tag_open_regexp="<g($| )"
	group_tag_close_regexp="</g>"
	rect_tag_open_regexp="<rect($| )"
	rect_tag_close_regexp="</rect>"
	image_tag_open_regexp="<image($| )"
	image_tag_close_regexp="</image>"
	tag_close_regexp="(^|[[:blank:]]*)/>($|[[:blank:]]*)"
}

NR==FNR {
	if ($0 ~ defs_tag_open_regexp)
		defs_open=1
	else if ($0 ~ group_tag_open_regexp)
		groups_open=1

	if (defs_open)
		array_defs[++array_defs[0]]=$0
	if (groups_open) {
		array_group[++array_group[0]]=$0
	}

	if ($0 ~ defs_tag_close_regexp)
		defs_open=0
	else if ($0 ~ group_tag_close_regexp)
		groups_open=0
	array_first_file[++array_first_file[0]]=$0
}
NR!=FNR {
	array_target_file[++array_target_file[0]]=$0
}

END{
	if (!(0 in array_target_file)) {
		delete array_target_file
		delete array_defs
		delete array_group
		for (i=0 ; i<=array_first_file[0] ; ++i)
			array_target_file[i]=array_first_file[i]
	}
	command_basename="basename \"" FILENAME "\""
	command_basename | getline filename
	close(command_basename)

	if (filename ~ "^(desktop|drive|mycomputer|mydocs|netdrive|printer)\.svg$") {
		transform_x="28"
		transform_y="16"
	}
	else {
		transform_x="20"
		transform_y="10"
	}
	
	if (filename ~ "^(msiexec|regedit|wcmd|winefile|winhelp)\.svg$")
		large_id_icon_regexp="id=\"icon\:32\-32\""
	else
		large_id_icon_regexp="id=\"icon\:48\-32\""
	if (filename ~ "^(iexplore|mycomputer|msiexec|notepad|regedit|taskmgr|wcmd|winecfg|winefile|winemine|winhelp|wordpad)\.svg$")
		suppress_group=1

	# Delete <image /> elements and smaller icon <rect id="icon:*-32" /><g>...</g> blocks from array
	icon_size=64
	for (target_line=1 ; target_line<=array_target_file[0] ; ++target_line) {
		svg_open=svg_open || (array_target_file[target_line] ~ svg_tag_open_regexp)
		if (svg_open) {
			sub("width=\"368\"", "width=\"64\"", array_target_file[target_line])
			sub("width=\"632\"", "width=\"352\"", array_target_file[target_line])
			if (sub("height=\"272\"", "height=\"352\"", array_target_file[target_line])) {
				icon_size=352
				insert_viewbox_offset=1
			}
			if (!update_inkscape_version)
				update_inkscape_version=sub("inkscape:version=\"0.4.*\"", "inkscape:version=\"0.92\"", array_target_file[target_line])
			if (array_target_file[target_line] ~ ">$") {
				svg_open=0
				insert_viewbox=(filename ~ "^(mycomputer)\.svg$")
			}
		}

		if (array_target_file[target_line] ~ rect_tag_open_regexp) {
			found_id_icon=found_large_id_icon=0
			for (line=target_line ; line <= array_target_file[0] ; ++line) {
				if (array_target_file[line] ~ "id=\"icon\:[[:digit:]]*\-[[:digit:]]*\"") {
					found_large_id_icon=(array_target_file[line] ~ large_id_icon_regexp)
					found_id_icon=1
				}
				if (found_id_icon && (icon_size == 64)) {
					sub("y=\"[\.[:digit:]]*\"", "y=\"8\"", array_target_file[line])
					sub("x=\"[\.[:digit:]]*\"", "x=\"8\"", array_target_file[line])
					sub("height=\"[\.[:digit:]]*\"", "height=\"48\"", array_target_file[line])
					sub("width=\"[\.[:digit:]]*\"", "width=\"48\"", array_target_file[line])
				}
				if (found_id_icon && (icon_size == 352)) {
					sub("\"icon\:[[:digit:]]*\-32\"", "\"icon:256-32\"")
					if (filename ~ "^(msiexec|notepad|regedit|taskmgr|wcmd|winecfg|winefile|winemine|winhelp|wordpad)\.svg$") {
						x=368 ; y=8
					}
					else {
						x=373 ; y=8
					}

					sub("y=\"[\.[:digit:]]*\"", ("y=\"" y "\""), array_target_file[line])
					sub("x=\"[\.[:digit:]]*\"", ("x=\"" x "\""), array_target_file[line])
					sub("height=\"[\.[:digit:]]*\"", "height=\"256\"", array_target_file[line])
					sub("width=\"[\.[:digit:]]*\"", "width=\"256\"", array_target_file[line])
				}
				if (array_target_file[line] ~ tag_close_regexp)
					break
			}
			if (found_id_icon) {
				if (!found_large_id_icon) {
					suppress_group=(filename !~ "(mycomputer)\.svg")
					target_line=line
					continue
				}
				suppress_group=(found_large_id_icon && (filename ~ "(control|oic_winlogo|printer)\.svg"))
			}
		}
		if (array_target_file[target_line] ~ group_tag_open_regexp) {
			++group_tag_depth
			group_open=1
		}

		image_tag_open=image_tag_open || (array_target_file[target_line] ~ image_tag_open_regexp)

		if (!(suppress_group && group_open) && !image_tag_open) {
			if (insert_viewbox) {
				array_processed_target_file[++array_processed_target_file[0]]="   viewBox=\"0 0 64 64\""
				insert_viewbox=0
			}
			else if (insert_viewbox_offset) {
				array_processed_target_file[++array_processed_target_file[0]]="   x=\"48\""
				array_processed_target_file[++array_processed_target_file[0]]="   y=\"48\""
				if (filename ~ "^(msiexec|notepad|regedit|taskmgr|wcmd|winecfg|winefile|winemine|winhelp|wordpad)\.svg$")
					array_processed_target_file[++array_processed_target_file[0]]="   viewBox=\"320 -40 352 352\""
				else
					array_processed_target_file[++array_processed_target_file[0]]="   viewBox=\"325 -40 352 352\""
				insert_viewbox_offset=0
			}
			array_processed_target_file[++array_processed_target_file[0]]=array_target_file[target_line]
		}
		image_tag_open=image_tag_open && (array_target_file[target_line] !~ tag_close_regexp)

		if (array_target_file[target_line] ~ group_tag_close_regexp) {
			--group_tag_depth
			group_open=(group_tag_depth > 0)
			suppress_group=suppress_group && group_open
		}
	}

	Dump remaining blocks of svg image - overlay reduced size wine logo
	for (target_line=1 ; target_line<=array_processed_target_file[0] ; ++target_line) {
		if (!defs_done && (array_processed_target_file[target_line] ~ defs_tag_close_regexp)) {
			# Insert <defs></defs> element from first file - strip tags
			for (i=2 ; i<array_defs[0] ; ++i)
				print array_defs[i] >target_path
			defs_done=1
		}
		else if (!group_done && (array_processed_target_file[target_line] ~ group_tag_close_regexp) \
				&& (target_line < array_processed_target_file[0]) \
				&& ((array_processed_target_file[target_line+1] ~ svg_tag_close_regexp) || (array_processed_target_file[target_line+1] ~ rect_tag_open_regexp))) {
			transformation_command=("transform=\"matrix(0.66,0,0,0.66," transform_x "," transform_y ")\"")
			match(array_group[1], group_tag_open_regexp)
			if (RSTART)
				printf("  %s%s %s\n", substr(array_group[1],RSTART,RLENGTH), transformation_command, substr(array_group[1],RSTART+RLENGTH)) >target_path
			else
				printf("  %s\n", array_group[1]) >target_path
			for (i=2 ; i<=array_group[0] ; ++i)
				printf("  %s\n", array_group[i]) >target_path
			group_done=1
		}
		print array_processed_target_file[target_line] >target_path
	}
}


