import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 用户状态管理 Store
 * 管理用户信息、认证状态和偏好设置
 */
export const useUserStore = defineStore('user', () => {
  // 用户基本信息
  const userId = ref<string>('')
  const username = ref<string>('')
  const email = ref<string>('')
  const avatar = ref<string>('')
  const githubToken = ref<string>('')

  // 认证状态
  const isAuthenticated = ref<boolean>(false)
  const isLoading = ref<boolean>(false)

  // 用户偏好设置
  const preferences = ref({
    language: 'zh-CN',
    timezone: 'Asia/Shanghai',
    notifications: true,
    emailDigest: true
  })

  /**
   * 设置用户信息
   */
  function setUser(userData: {
    id: string
    username: string
    email: string
    avatar?: string
    githubToken?: string
  }) {
    userId.value = userData.id
    username.value = userData.username
    email.value = userData.email
    avatar.value = userData.avatar || ''
    githubToken.value = userData.githubToken || ''
    isAuthenticated.value = true
  }

  /**
   * 更新GitHub Token
   */
  function updateGithubToken(token: string) {
    githubToken.value = token
  }

  /**
   * 更新用户偏好设置
   */
  function updatePreferences(prefs: Partial<typeof preferences.value>) {
    preferences.value = { ...preferences.value, ...prefs }
  }

  /**
   * 登出
   */
  function logout() {
    userId.value = ''
    username.value = ''
    email.value = ''
    avatar.value = ''
    githubToken.value = ''
    isAuthenticated.value = false
  }

  /**
   * 从localStorage恢复用户状态
   */
  function restoreUserState() {
    try {
      const savedUser = localStorage.getItem('user')
      const savedPreferences = localStorage.getItem('userPreferences')
      
      if (savedUser) {
        const userData = JSON.parse(savedUser)
        setUser(userData)
      }
      
      if (savedPreferences) {
        preferences.value = JSON.parse(savedPreferences)
      }
    } catch (error) {
      console.error('Failed to restore user state:', error)
    }
  }

  /**
   * 保存用户状态到localStorage
   */
  function saveUserState() {
    try {
      const userData = {
        id: userId.value,
        username: username.value,
        email: email.value,
        avatar: avatar.value,
        githubToken: githubToken.value
      }
      localStorage.setItem('user', JSON.stringify(userData))
      localStorage.setItem('userPreferences', JSON.stringify(preferences.value))
    } catch (error) {
      console.error('Failed to save user state:', error)
    }
  }

  return {
    // State
    userId,
    username,
    email,
    avatar,
    githubToken,
    isAuthenticated,
    isLoading,
    preferences,
    
    // Actions
    setUser,
    updateGithubToken,
    updatePreferences,
    logout,
    restoreUserState,
    saveUserState
  }
})