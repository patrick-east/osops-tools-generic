#!/usr/bin/env bash

ls ~/projects/cinder_jenkins_data/puppet/pc2/nodes | sed 's/\.pp//g' | xargs -n1 -I {} bash -c "./fc_detach.sh {} || True"
