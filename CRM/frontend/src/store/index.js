import { createStore } from 'vuex'

export default createStore({
  state: {
    isLoggedIn: false,
    userName: '',
    userAvatar: '',
    userInfo: null
  },
  mutations: {
    SET_LOGIN_STATUS(state, status) {
      state.isLoggedIn = status
    },
    SET_USER_INFO(state, userInfo) {
      state.userName = userInfo?.name || ''
      state.userAvatar = userInfo?.avatar || ''
      state.userInfo = userInfo
    },
    LOGOUT(state) {
      state.isLoggedIn = false
      state.userName = ''
      state.userAvatar = ''
      state.userInfo = null
    }
  },
  actions: {
    login({ commit }, userInfo) {
      commit('SET_LOGIN_STATUS', true)
      commit('SET_USER_INFO', userInfo)
    },
    logout({ commit }) {
      commit('LOGOUT')
    },
    updateUserInfo({ commit }, userInfo) {
      commit('SET_USER_INFO', userInfo)
    }
  },
  getters: {
    isAuthenticated: state => state.isLoggedIn,
    currentUser: state => state.userInfo
  }
})
