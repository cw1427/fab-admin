export type UserLoginType = {
  userName: string
  password: string
}

export type UserType = {
  userName: string
  password: string
  role: string
  roleId: string
  permissions: string | string[]
}
