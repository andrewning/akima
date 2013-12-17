

subroutine setup(n, xpt, ypt, p0, p1, p2, p3)
    implicit none

    integer, parameter :: ReKi = selected_real_kind(15, 307)
    real(ReKi), parameter :: eps = 1d-30

    ! in
    integer, intent(in) :: n
    real(ReKi), dimension(n), intent(in) :: xpt, ypt  ! given points

    ! out
    real(ReKi), dimension(n-1), intent(out) :: p0, p1, p2, p3  ! spline coefficients

    ! local
    integer :: i
    real(ReKi), dimension(-1:n+1) :: m
    real(ReKi), dimension(n) :: t
    real(ReKi) :: m1, m2, m3, m4, w1, w2
    real(ReKi) :: t1, t2, dx

    ! compute segment slopes
    do i = 1, n-1
        m(i) = (ypt(i+1) - ypt(i)) / (xpt(i+1) - xpt(i))
    end do

    ! estimation for end points
    m(0) = 2*m(1) - m(2)
    m(-1) = 2*m(0) - m(1)
    m(n) = 2*m(n-1) - m(n-2)
    m(n+1) = 2*m(n) - m(n-1)

    ! slope at points
    do i = 1, n
        m1 = m(i-2)
        m2 = m(i-1)
        m3 = m(i)
        m4 = m(i+1)
        w1 = abs(m4 - m3)
        w2 = abs(m2 - m1)
        if ( w1 < eps .and. w2 < eps ) then
            t(i) = 0.5*(m2 + m3)  ! special case to avoid divide by zero
        else
            t(i) = (w1*m2 + w2*m3) / (w1 + w2)
        end if
    end do

    ! polynomial cofficients
    do i = 1, n-1
        dx = xpt(i+1) - xpt(i)
        t1 = t(i)
        t2 = t(i+1)
        p0(i) = ypt(i)
        p1(i) = t1
        p2(i) = (3.0*m(i) - 2.0*t1 - t2)/dx
        p3(i) = (t1 + t2 - 2.0*m(i))/dx**2
    end do


end subroutine setup


subroutine interp(npt, xpt, p0, p1, p2, p3, n, x, y, dydx)
    implicit none
    integer, parameter :: ReKi = selected_real_kind(15, 307)

    ! in
    integer, intent(in) :: npt
    real(ReKi), dimension(npt), intent(in) :: xpt  ! given x points
    real(ReKi), dimension(npt-1), intent(in) :: p0, p1, p2, p3  ! spline coefficients
    integer, intent(in) :: n
    real(ReKi), dimension(n), intent(in) :: x  ! x values to evalute at

    ! out
    real(ReKi), dimension(n), intent(out) :: y  ! interpolate y values
    real(ReKi), dimension(n), intent(out) :: dydx  ! derivative of y w.r.t. x

    ! local
    integer :: i, j
    real(ReKi) :: dx

     ! interpolate at each point
    do i = 1, n

        ! find location in array (use end segments if out of bounds)
        if (x(i) < xpt(1)) then
            j = 1

        else
            ! linear search for now
            do j = npt-1, 1, -1
                if ( x(i) >= xpt(j)) then
                    exit
                end if
            end do
        end if

        ! evaluate polynomial (and derivative)
        dx = (x(i) - xpt(j))
        y(i) = p0(j) + p1(j)*dx + p2(j)*dx**2 + p3(j)*dx**3
        dydx(i) = p1(j) + 2*p2(j)*dx + 3*p3(j)*dx**2


    end do


end subroutine interp