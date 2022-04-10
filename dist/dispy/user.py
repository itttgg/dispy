import dist.dispy.http.rest


class _UserBase:
    def __init__(self, id, rest: dist.dispy.http.rest.Rest, premium_gets):
        self.id = id
        self._rest = rest

        # Data
        _data = self._rest.get("user", self.id)
        if premium_gets:
            try:
                _premium_type = int(_data["premium_type"])
            except KeyError:
                _premium_type = -1
                raise dist.dispy.errs.MissingPerms(dist.dispy.errs.missingperms)

            self.username = _data["username"]
            self.discriminator = _data["discriminator"]
            self.fullname = f"{self.username}#{self.discriminator}"

            try:
                self.isbot: bool = _data["bot"]
            except KeyError:
                del self.isbot
                raise dist.dispy.errs.MissingPerms(dist.dispy.errs.missingperms)

            try:
                self.issystem: bool = _data["system"]
            except KeyError:
                del self.issystem
                raise dist.dispy.errs.MissingPerms(dist.dispy.errs.missingperms)

            try:
                self.isverified: bool = _data["verified"]  # May be ""
            except KeyError:
                del self.isverified
                raise dist.dispy.errs.MissingPerms(dist.dispy.errs.missingperms)

            try:
                self.email: bool = _data["email"]  # May be ""
            except KeyError:
                del self.email
                raise dist.dispy.errs.MissingPerms(dist.dispy.errs.missingperms)

            self.flags: int = int(_data["public_flags"])

            self.nitro = DisNitro(_premium_type, _premium_type != 0 and _premium_type != -1)
        else:
            _premium_type = -1
            self.flags: int = int(_data["public_flags"])
            self.username = _data["username"]
            self.discriminator = _data["discriminator"]
            self.fullname = f"{self.username}#{self.discriminator}"

    def uptade(self) -> None:
        _data = self._rest.get("user", self.id)

        try:
            _premium_type = int(_data["premium_type"])
        except KeyError:
            _premium_type = -1

        self.username = _data["username"]
        self.discriminator = _data["discriminator"]
        self.fullname = f"{self.username}{str(self.discriminator)}"
        try:
            self.isbot: bool = _data["bot"]
            self.issystem: bool = _data["system"]
            self.isverified: bool = _data["verified"]  # May be ""
            self.email: bool = _data["email"]  # May be ""
        except KeyError:
            pass

        self.flags: int = int(_data["public_flags"])

        try:
            self.nitro = DisNitro(_premium_type, _premium_type != 0 and _premium_type != -1)
        except UnboundLocalError:
            pass


class DisUser(_UserBase):
    def __init__(self, id, rest, premium_gets):
        super().__init__(id, rest, premium_gets)


class DisNitro:
    def __init__(self, type, ishave):
        self.classic = "classic"
        self.boost = "boost"
        self.none = "none"
        if type != -1:
            self.have = ishave
        else:
            del self.have
        if type == 1:
            self.type = self.classic
        elif type == 2:
            self.type = self.boost
        elif type == -1:
            raise dist.dispy.errs.MissingPerms(dist.dispy.errs.missingperms)
        elif type == 0:
            self.type = self.none
        else:
            raise dist.dispy.errs.UserNitroTypeError("Invalid type of error!")