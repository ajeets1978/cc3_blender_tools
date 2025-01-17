# Copyright (C) 2021 Victor Soupday
# This file is part of CC3_Blender_Tools <https://github.com/soupday/cc3_blender_tools>
#
# CC3_Blender_Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CC3_Blender_Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CC3_Blender_Tools.  If not, see <https://www.gnu.org/licenses/>.

import json
import os

from . import utils


def read_json(fbx_path):
    try:
        fbx_file = os.path.basename(fbx_path)
        fbx_folder = os.path.dirname(fbx_path)
        fbx_name = os.path.splitext(fbx_file)[0]
        json_path = os.path.join(fbx_folder, fbx_name + ".json")
        if os.path.exists(json_path):
            file = open(json_path, "rt")
            # json files outputted from Visual Studio projects start with a byte mark order block (3 bytes EF BB BF)
            file.seek(3)
            text_data = file.read()
            json_data = json.loads(text_data)
            utils.log_info("Json data read: " + json_path)
            return json_data
        utils.log_info("No Json data to parse, using defaults...")
        return None
    except:
        utils.log_warn("Failed to read Json data: " + json_path)
        return None

def get_character_generation_json(character_json, file_name, character_id):
    try:
        return character_json[file_name]["Object"][character_id]["Generation"]
    except:
        utils.log_warn("Failed to read character generation data!")
        return None

def get_character_root_json(json_data, file_name):
    if not json_data:
        return None
    try:
        return json_data[file_name]["Object"]
    except:
        utils.log_warn("Failed to get character root Json data!")
        return None

def get_character_json(json_data, file_name, character_id):
    if not json_data:
        return None
    try:
        character_json = json_data[file_name]["Object"][character_id]
        utils.log_info("Character Json data found for: " + character_id)
        return character_json
    except:
        utils.log_warn("Failed to get character Json data!")
        return None

def get_object_json(character_json, obj):
    if not character_json:
        return None
    try:
        name = obj.name.lower()
        meshes_json = character_json["Meshes"]
        for object_name in meshes_json.keys():
            if object_name.lower() in name:
                utils.log_info("Object Json data found for: " + obj.name)
                return meshes_json[object_name]
    except:
        utils.log_warn("Failed to get object Json data!")
        return None

def get_custom_shader(material_json):
    try:
        return material_json["Custom Shader"]["Shader Name"]
    except:
        try:
            return material_json["Material Type"]
        except:
            utils.log_warn("Failed to material shader data!")
            return "Pbr"

def get_material_json(object_json, material):
    if not object_json:
        return None
    try:
        name = material.name.lower()
        materials_json = object_json["Materials"]
        for material_name in materials_json.keys():
            if material_name.lower() in name:
                utils.log_info("Material Json data found for: " + material.name)
                return materials_json[material_name]
    except:
        utils.log_warn("Failed to get material Json data!")
        return None

def get_texture_info(material_json, texture_id):
    tex_info = get_pbr_texture_info(material_json, texture_id)
    if tex_info is None:
        tex_info = get_shader_texture_info(material_json, texture_id)
    return tex_info

def get_pbr_texture_info(material_json, texture_id):
    if not material_json:
        return None
    try:
        return material_json["Textures"][texture_id]
    except:
        return None

def get_shader_texture_info(material_json, texture_id):
    if not material_json:
        return None
    try:
        return material_json["Custom Shader"]["Image"][texture_id]
    except:
        return None

def get_material_json_var(material_json, var_path: str):
    var_type, var_name = var_path.split('/')
    if var_type == "Custom":
        return get_shader_var(material_json, var_name)
    elif var_type == "SSS":
        return get_sss_var(material_json, var_name)
    elif var_type == "Pbr":
        return get_pbr_var(material_json, var_name)
    else: # var_type == "Base":
        return get_material_var(material_json, var_name)


def get_shader_var(material_json, var_name):
    if not material_json:
        return None
    try:
        return material_json["Custom Shader"]["Variable"][var_name]
    except:
        return None

def get_pbr_var(material_json, var_name):
    if not material_json:
        return None
    try:
        return material_json["Textures"][var_name]["Strength"] / 100.0
    except:
        return None

def get_material_var(material_json, var_name):
    if not material_json:
        return None
    try:
        return material_json[var_name]
    except:
        return None

def get_sss_var(material_json, var_name):
    if not material_json:
        return None
    try:
        return material_json["Subsurface Scatter"][var_name]
    except:
        return None

def convert_to_color(json_var):
    if type(json_var) == list:
        for i in range(0, len(json_var)):
            json_var[i] /= 255.0
        if len(json_var) == 3:
            json_var.append(1)
    return json_var

def get_shader_var_color(material_json, var_name):
    if not material_json:
        return None
    try:
        json_color = material_json["Custom Shader"]["Variable"][var_name]
        return convert_to_color(json_color)
    except:
        return None

