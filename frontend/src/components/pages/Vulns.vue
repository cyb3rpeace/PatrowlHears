<template>
  <div>

    <v-card>
      <v-card-title class="py-0">
        <!-- Vulnerabilities -->
        <v-container>
          <v-row>
            <v-col class="pa-2" md="auto" >
              Vulnerabilities<br/>
              <v-chip
                small label 
                outlined 
                :color="getBoolColor(this.show_all)"
                @click="toggleShowAll()"
              >All</v-chip>&nbsp;
              <v-chip
                small label 
                outlined 
                :color="getBoolColor(this.show_last_day)"
                @click="toggleShowLastDay()"
              >Last 24h</v-chip>&nbsp;
              <v-chip
                small label 
                outlined 
                :color="getBoolColor(this.show_last_week)"
                @click="toggleShowLastWeek()"
              >Last Week</v-chip>&nbsp;
              <v-chip
                small label 
                outlined 
                :color="getBoolColor(this.show_monitored)"
                @click="toggleMonitored()"
              >Monitored</v-chip>
            </v-col>
            <v-col class="pa-2" md="4">
              <v-text-field
                class="pt-0"
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
              />
            </v-col>
            <v-col class="pa-2 mt-4" md="3">
              <v-range-slider
                v-model="search_slider"
                label="Score"
                max="100"
                min="0"
                thumb-label
                thumb-color="deep-orange"
                track-color="grey"
                color="deep-orange"
              ></v-range-slider>
            </v-col>
          </v-row>
          <v-row v-if="showAdvancedFilters">
            <v-col cols="12">
              <v-divider></v-divider>
              <advanced-search scope='vulns' v-on:advanced_search_filters="updateAdvancedSearchFilters"></advanced-search>
            </v-col>
          </v-row>
        </v-container>
      </v-card-title>

      <v-btn
        depressed tile block
        v-if="!showAdvancedFilters"
        @click="showAdvancedFilters=true"
        label="coic"
      >
        <v-icon>mdi-chevron-down</v-icon>Show advanced filters<v-icon>mdi-chevron-down</v-icon>
      </v-btn>

      <v-btn
        depressed tile block
        v-else
        @click="showAdvancedFilters=!showAdvancedFilters"
        label="coic"
      >
        <v-icon>mdi-chevron-up</v-icon>Hide advanced filters<v-icon>mdi-chevron-up</v-icon>
      </v-btn>

      <v-data-table
        :headers="headers"
        :search="search"
        :items="vulns.results"
        :server-items-length="vulns.count"
        :options.sync="options"
        :items-per-page="limit"
        :footer-props="{
          'items-per-page-options': rowsPerPageItems
        }"
        :loading="loading"
        class="elevation-4"
        item-key="id"
        multi-sort
      > 

        <!-- Rating --> 
        <template v-slot:[`item.score`]="{ item }">
          <v-chip
            :color="getRatingColor(item.score)"
            class="text-center font-weight-bold"
            label
          >{{item.score}}/100</v-chip><br/>
          <span class="text-caption">CVSSv2: {{item.cvss}}</span><br/>
          <span class="text-caption">CVSSv3: {{item.cvss3}}</span>
        </template>

        <!-- Summary --> 
        <template v-slot:[`item.summary`]="{ item }">
          <div class="py-2">
            <div class="pb-2">
              <span class="deep-orange--text font-weight-medium">{{item.cveid}}</span> / PH-{{item.id}}
              <v-btn
                color="deep-orange"
                icon small
              >
                <v-icon title="View details" @click="viewVuln(item.id)">mdi-arrow-right-bold-circle-outline</v-icon>
              </v-btn>
            </div>
            <div>
              {{item.summary}}
            </div>
            <v-chip
              v-for="p in item.products.slice(0, 5)" :key="p.id"
              class="vendor-chip"
              label small link
              @click="$router.push({ 'path': '/product/'+p.id });"
            >
              {{ p.vendor }}: <span class="font-weight-bold">{{p.name}}</span>
            </v-chip>
            <span v-if="item.products.length > 5" @click="viewVuln(item.id)">+</span>
          </div>
        </template>

        <!-- Metadata -->
        <template v-slot:[`item.metadata`]="{ item }">
          <!-- Is exploitable -->
          <v-chip
            label link small
            :color="item.exploit_count>0?'deep-orange':'grey'"
            class="font-weight-bold"
            title="Is exploitable?"
          >
            {{item.exploit_count}}
          </v-chip>
  
          <!-- Remotely exploitable -->
          <v-btn
            :color="item.access.vector=='NETWORK'?'deep-orange':'grey'"
            icon small
          >
            <v-icon title="Is exploitable remotely?">mdi-cloud</v-icon>
          </v-btn>
  
          <!-- Auth Needed -->
          <v-btn
            :color="item.access.authentication=='NONE'?'deep-orange':'grey'"
            icon small
          >
            <v-icon title="Require authentication?">mdi-shield-account</v-icon>
          </v-btn>
  
          <!-- In the News/Wild -->
          <v-btn
            :color="item.is_in_the_news||item.is_in_the_wild?'deep-orange':'grey'"
            icon small
          >
            <v-icon title="Is in the news or exploited in the wild?">mdi-star</v-icon>
          </v-btn>
        </template>

        <!-- Monitored -->
        <template v-slot:[`item.monitored`]="{ item }">
          <v-chip
            small label outlined :color="getBoolColor(true)"
            class="text-center font-weight-bold"
            @click="toggleMonitoredVuln(item)"
            v-if="item.monitored"
          >Yes</v-chip>
          <v-chip
            small label outlined :color="getBoolColor(false)"
            class="text-center font-weight-bold"
            @click="toggleMonitoredVuln(item)"
            v-if="!item.monitored"
          >No</v-chip>
        </template>

        <!-- Updated at -->
        <template v-slot:[`item.updated_at`]="{ item }">
          <span>{{moment(item.updated_at).format('YYYY-MM-DD, hh:mm')}}</span>
        </template>
      </v-data-table>

      <v-dialog v-model="dialog_vuln" max-width="600px" v-if="this.showManageMetadataButtons()">
        <template v-slot:activator="{ on }">
          <v-btn absolute dark fab bottom left color="deep-orange" v-on="on">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        <DialogVulnAddEdit />
      </v-dialog>

      <v-snackbar v-model="snack.open" :timeout="3000" :color="snack.color" dense>
        {{ snack.text }}
        <v-btn text @click="snack.open = false">Close</v-btn>
      </v-snackbar>

    </v-card>
    
  </div>
</template>

<script>
import Colors from "../../common/colors";
import Users from "../../common/users";
import DialogVulnAddEdit from '@/components/vulnerability/vulnerabilityDetails/dialog/DialogVulnAddEdit.vue';
import AdvancedSearch from '@/components/pages/AdvancedSearch.vue';
import _ from 'lodash';
import moment from 'moment';

export default {
  name: "vulns",
  mixins: [Colors, Users],
  components: {
    DialogVulnAddEdit,
    AdvancedSearch
  },
  data: () => ({
    vulns: [],
    loading: true,
    limit: 10,
    search: '',
    showAdvancedFilters: false,
    advancedSearchFilter: null,
    show_all: true,
    show_last_day: false,
    show_last_week: false,
    show_monitored: false,
    search_slider: [0,100],
    options: {},
    headers: [
      { text: 'Score', value: 'score', align: 'center', width: "10%" },
      { text: 'Summary', value: 'summary' },
      { text: 'Metadata', value: 'metadata', align: 'center', width: "8%", sortable: false },
      { text: 'Monitored', value: 'monitored', align: 'center', },
      { text: 'Last update', value: 'updated_at', align: 'center', width: "12%" },
    ],
    rowsPerPageItems: [5, 10, 20, 50, 100],
    dialog_vuln: false,
    snack: {
      open: false, 
      color: '',
      text: ''
    }
  }),
  watch: {
    search: _.debounce(function (filter) {
      this.search = filter;
      this.options.page = 1;  // reset page count
      this.getDataFromApi();
    }, 500),
    options: {
      handler() {
        this.getDataFromApi();
      },
      deep: true
    },
    search_slider: _.debounce(function () {
      this.getDataFromApi();
    }, 500),
    show_all: {
      handler() {
        this.getDataFromApi();
      },
      deep: true
    },
    show_last_day: {
      handler() {
        this.getDataFromApi();
      },
      deep: true
    },
    show_last_week: {
      handler() {
        this.getDataFromApi();
      },
      deep: true
    },
    show_monitored: {
      handler() {
        this.getDataFromApi();
      },
      deep: true
    }
  },
  methods: {
    getDataFromApi(page_id) {
      this.loading = true;
      // console.log(page_id)

      return new Promise((resolve, reject) => {
        let {
          sortBy,
          sortDesc,
          page,
          itemsPerPage
        } = this.options;
        if (page_id != null && page_id != '') {
          page = page_id;
        }
        let search = this.search.trim().toLowerCase();

        this.limit = itemsPerPage;
        let items = this.getVulns(page, this.limit, sortBy, sortDesc);

        setTimeout(() => {
          resolve({
            items
          });
        }, 300);
      });
      this.loading = false;
    },
    updateAdvancedSearchFilters(filters){
      this.advancedSearchFilter = filters
      this.getDataFromApi();
    },
    getVulns(page, itemsPerPage, sortBy, sortDesc) {
      let sorted_by = '';
      if (sortBy.length > 0) {
        if (sortDesc[0] === true) {
          sorted_by = 'sorted_by=-' + sortBy;
        } else {
          sorted_by = 'sorted_by=' + sortBy;
        }
      }

      let filter_by_date = '';
      if (this.show_last_day == true) {
        filter_by_date = "&updated_at__gte=" + moment(new Date()).format('YYYY-MM-DD');
      } else if (this.show_last_week == true) {
        filter_by_date = "&updated_at__gte=" + moment(new Date()).subtract(7 , 'day').format('YYYY-MM-DD');
      }

      let extra_filters = "&score__gte="+this.search_slider[0]+"&score__lte="+this.search_slider[1]
      if (this.advancedSearchFilter != null) {
        extra_filters += this.advancedSearchFilter
      }

      let url = '/api/vulns/?limit='+itemsPerPage+'&page='+page+'&search='+this.search+'&'+sorted_by+filter_by_date+extra_filters

      if (this.show_monitored === true) {
        url = url + "&monitored=true"
      }

      this.$api.get(url).then(res => {
        this.vulns = res.data;
        this.loading = false;
        return this.vulns;
      }).catch(e => {
        this.vulns = [];
        this.loading = false;
        this.snack = {
          open: true,
          color: "error",
          text: 'Unable to get vulns.'
        }
      });
    },
    viewVuln(vuln_id) {
      this.$router.push({ 'name': 'Vuln', 'params': { 'vuln_id': vuln_id } });
    },
    showManageMetadataButtons(){
      let p = JSON.parse(this.getUserProfile());
      if (p != null && 'manage_metadata' in p){
          return p.manage_metadata;
      } else {
        return true;
      }
    },
    toggleMonitoredVuln(item) {
      // save in backend
      let data = {
        'monitored': !item.monitored,
        'vuln_id': item.id,
        'organization_id': localStorage.getItem('org_id')
      };

      this.$api.put('/api/vulns/'+item.id+'/toggle', data).then(res => {
        if (res){
          item.monitored = !item.monitored;
          // Snack notifications
          this.snack = {
            open: true,
            color: 'success',
            text: 'Vulnerability monitoring successfuly updated.'
          }
        } else {
          this.snack = {
            snack: true, 
            color: 'error',
            text: 'Unable to change the vulnerability monitoring status'
          }
        }
      }).catch(e => {
        this.loading = false;
        swal.fire({
          title: 'Error',
          text: 'Unable to change the vulnerability monitoring status',
          showConfirmButton: false,
          showCloseButton: false,
          timer: 3000
        });
        return;
      });
    },
    toggleMonitored() {
      if (this.show_monitored === true) {
        this.show_monitored = false;
      } else {
        this.show_monitored = true;
      }
    },
    toggleShowAll() {
      this.options.page = 1;
      if (this.show_all == false) {
        this.show_all = !this.show_all;
      }
      if (this.show_all == true) {
        this.show_last_day = false;
        this.show_last_week = false;
      }
    },
    toggleShowLastDay() {
      this.options.page = 1;
      if (this.show_last_day == true) {
        this.show_all = true;
        this.show_last_day = false;
        this.show_last_week = false;
      }
      if (this.show_last_day == false) {
        this.show_last_day = true;
        this.show_all = false;
        this.show_last_week = false;
      }
    },
    toggleShowLastWeek() {
      this.options.page = 1;
      if (this.show_last_week == true) {
        this.show_all = true;
        this.show_last_day = false;
        this.show_last_week = false;
      }
      if (this.show_last_week == false) {
        this.show_last_week = true;
        this.show_all = false;
        this.show_last_day = false;
      }
    },
    editVuln(vuln_id) {
      // Todo
    },
    deleteVuln(vuln_id) {
      // Todo
    },
  }
};
</script>

<style>
.v-data-table td, .v-data-table th {
    padding: 0 8px;
}
.v-dialog {
    position: absolute;
    left: 0;
}
.vendor-chip {
  padding-right: 5px;
  padding-left: 5px;
  margin-right: 3px;
}
.v-chip.v-size--small {
  border-radius: 12px;
  font-size: 12px;
  height: 20px;
}
</style>
