#!/bin/bash

# config.bash v1.0 @ 2024-11-02 - nelbren@nelbren.com

myEcho() {
    tag="$1"
    printf "$tag${S}\n"
}

colors_set() {
    S="\e[0m";E="\e[K";n="$S\e[38;5";N="\e[9";e="\e[7";I="$e;49;9"
    A=7m;R=1m;G=2m;Y=3m;nW="$N$A";nR="$N$R";nG="$N$G";nY="$N$Y"
    Iw="$I$A";Ir="$I$R";Ig="$I$G";Iy="$I$Y" 
}

my_set_env_install() {
    printf "${nW}my_set_env.bash...${S}"
    if [ ! -r my_set_env.bash ]; then
        myEcho ${nY}'☐'
        printf "\n${Iw}cp my_set_env.bash.example my_set_env.bash${S}\n"
        cp my_set_env.bash.example my_set_env.bash
        if [ ! -r my_set_env.bash ]; then
            myEcho ${nR}'×'
            printf "\n${nY}Please manually copy config! ( cp my_set_env.bash.example my_set_env.bash )${S}\n"
            exit 1
        fi 
    else
        myEcho ${nG}'✓'
        printf "${nW}INSTRUCTURE_URL...${S}"
        if grep -q replace-with-your-INFRASTRUCTURE-URL_and_rename_this_file my_set_env.bash; then
            myEcho ${nR}'×'
            printf "\n${nY}Change INSTRUCTURE_URL in my_set_env.bash!${S}\n"
            exit 2
        else
            myEcho ${nG}'✓'
        fi
        printf "${nW}API_KEY...........${S}"
        if grep -q replace-with-your-KEY_API_and_rename_this_file my_set_env.bash; then
            myEcho ${nR}'×'
            printf "\n${nY}Change API_KEY in my_set_env.bash!${S}\n"
            exit 3
        else
            myEcho ${nG}'✓'
        fi
    fi
}

colors_set
my_set_env_install