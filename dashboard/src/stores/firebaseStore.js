import { defineStore }      from 'pinia';
import { initializeApp }    from 'firebase/app';
import { processRelayData } from './dataProcessor';
import {
  getDatabase
  , ref
  , query
  , orderByKey
  , limitToLast
  , onValue
} from "firebase/database";

const firebaseConfig = {
  apiKey: "AIzaSyCptDiH85U6qnuzpeDPQRPhziqLOVEWOZc",
  authDomain: "esp32-9311c.firebaseapp.com",
  databaseURL: "https://esp32-9311c-default-rtdb.firebaseio.com",
  projectId: "esp32-9311c",
  storageBucket: "esp32-9311c.appspot.com",
  messagingSenderId: "420084515626",
  appId: "1:420084515626:web:dbec77bc2a4af3e1fb1453"
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

export const useFirebaseStore = defineStore('firebase', {
  state: () => ({
    relayData: JSON.parse(localStorage.getItem('relayData')) || null,
    processData: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchRelayData(limit = 15) {
      this.loading = true;
      try {
        const dbRef = ref(database, 'equip001');
        const queryRef = query(dbRef, orderByKey(), limitToLast(limit));
        onValue(queryRef, (snapshot) => {
          if (snapshot.exists()) {
            console.log('chamando firebase', snapshot.val());
            this.relayData = Object.entries(snapshot.val()).map(([, value]) => ({ ...value }));
            localStorage.setItem('relayData', JSON.stringify(this.relayData));
            this.getProcessedData();
          } else {
            console.log("Firebase: no data available");
            this.relayData = null;
          }
        });
      } catch (error) {
        console.error(error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    getProcessedData() {
      if (this.relayData || JSON.parse(localStorage.getItem('relayData'))) {
        this.processData = processRelayData(this.relayData || JSON.parse(localStorage.getItem('relayData')));
        return this.processData;
      }
      return null;
    }
  },
});
